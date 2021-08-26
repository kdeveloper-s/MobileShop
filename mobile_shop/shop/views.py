from django.core import paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from django.db.models.fields import NullBooleanField
from django.db.models.query import EmptyQuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

from .models import *

from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def home(request):
	products = Product.objects.all().order_by('-price')[:8]

	context = {
		'products': products,
	}
	return render(request, "home.html", context)


def products(request, category_slug=None):
	categories = None
	products = None

	if category_slug != None:
		categories = get_object_or_404(Category, slug=category_slug)
		products = Product.objects.filter(category=categories)
		paginator = Paginator(products, 21)
		page = request.GET.get('page')
		paged_products = paginator.get_page(page)
		product_count = products.count()
	else:
		products = Product.objects.all()
		paginator = Paginator(products, 21)
		page = request.GET.get('page')
		paged_products = paginator.get_page(page)
		product_count = products.count()
	
	context = {
		'products': paged_products,
		'product_count': product_count,
	}
	return render(request, "shop/products.html", context)


def product_detail(request, category_slug, product_slug):
	try:
		single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
	except Exception as e:
		raise e
	context = {
		'single_product': single_product,
		'in_cart': in_cart,
	}
	return render(request, "shop/product_detail.html", context)


def search(request):
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		if keyword:
			products = Product.objects.filter(name__icontains=keyword)
			product_count = products.count()
		context = {
			'products': products,
			'product_count': product_count,
		}
	return render(request, 'shop/products.html', context)


def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart


def add_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(
			cart_id = _cart_id(request)
		)
	cart.save()

	try:
		cart_item = CartItem.objects.get(product=product, cart=cart)
		cart_item.quantity += 1
		cart_item.save()
	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(
			product = product,
			quantity = 1,
			cart = cart,
		)
	cart_item.save()
	return redirect('cart')


def remove_cart(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart')


def remove_cart_item(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
	try:
		shipping = 0
		grand_total = 0
		if request.user.is_authenticated:
			cart_items = CartItem.objects.filter(user=request.user, is_active=True)
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart, is_active=True)
		for cart_item in cart_items:
			total += (int(float(cart_item.product.price)) * cart_item.quantity)
			quantity += cart_item.quantity
		shipping = 9.99
		grand_total = total + shipping
	except ObjectDoesNotExist:
		pass

	context = {
		'total': total,
		'quantity': quantity,
		'cart_items': cart_items,
		'shipping': shipping,
		'grand_total': grand_total,
	}
	return render(request, "shop/cart.html", context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
	try:
		shipping = 0
		grand_total = 0
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, is_active=True)
		for cart_item in cart_items:
			total += (int(float(cart_item.product.price)) * cart_item.quantity)
			quantity += cart_item.quantity
		shipping = 9.99
		grand_total = total + shipping
	except ObjectDoesNotExist:
		pass

	context = {
		'total': total,
		'quantity': quantity,
		'cart_items': cart_items,
		'shipping': shipping,
		'grand_total': grand_total,
	}
	return render(request, "shop/checkout.html", context)


def guide(request):
    return render(request, "shop/guide.html")


def register(request):
    return render(request, "shop/register.html")


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")

			# ----------------------------------------------------

			subject = "Registration successful."
			email_template_name = "password/new_user_greeting.txt"
			c = {
			"email":user.email,
			'domain':'127.0.0.1:8000',
			'site_name': 'MobileShop',
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),
			"user": user,
			'token': default_token_generator.make_token(user),
			'protocol': 'http',
			}
			email = render_to_string(email_template_name, c)
			try:
				send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			# ----------------------------------------------------

			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="registration/register_request.html", context={"register_form": form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				try:
					cart = Cart.objects.get(cart_id=_cart_id(request))
					is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
					if is_cart_item_exists:
						cart_item = CartItem.objects.filter(cart=cart)
						for item in cart_item:
							item.user = user
							item.save()
				except:
					pass
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login_request.html", context={"login_form": form})


@login_required(login_url='login')
def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("/")


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'MobileShop',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def password_reset_done(request):
	print(f'Request::: {request}')
	return render(request=request, template_name="password/password_reset_done.html")
	# return HttpResponse('Password reset link sent!')