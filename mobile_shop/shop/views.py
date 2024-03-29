from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

import requests
import pandas as pd
from django.conf import settings


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
	else:
		products = Product.objects.all()
	paginator = Paginator(products, 21)
	page = request.GET.get('page')
	paged_products = paginator.get_page(page)
	product_count = products.count()

	current_user = request.user
	if current_user.is_authenticated:
		in_cart = CartItem.objects.filter(user=current_user)
		cart_product_ids = [x.product.id for x in in_cart]
	else:
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request))
		cart_product_ids = [x.product.id for x in in_cart]

	context = {
		'products': paged_products,
		'product_count': product_count,
		'cart_product_ids': cart_product_ids,
	}
	return render(request, "shop/products.html", context)


def product_detail(request, category_slug, product_slug):
	current_user = request.user
	single_product = Product.objects.get(
		category__slug=category_slug, slug=product_slug)
	if current_user.is_authenticated:
		in_cart = CartItem.objects.filter(
			user=current_user, product=single_product).exists()
	else:
		in_cart = CartItem.objects.filter(
			cart__cart_id=_cart_id(request), product=single_product).exists()
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
	current_user = request.user
	product = Product.objects.get(id=product_id)
	category_slug = product.category.slug
	product_slug = product.slug
	request_from = request.GET.get("from")
	if current_user.is_authenticated:
		try:
			cart_item = CartItem.objects.get(product=product, user=current_user)
			cart_item.quantity += 1
			cart_item.save()
			return redirect('cart')
		except CartItem.DoesNotExist:
			cart_item = CartItem.objects.create(
				product=product,
				quantity=1,
				user=current_user,
			)
			cart_item.save()
			if request_from == "single_product":
				return redirect(reverse('product_detail', kwargs={"category_slug": category_slug, "product_slug": product_slug, }))
			else:
				return redirect(reverse('products_by_category', kwargs={"category_slug": category_slug}))
	else:
		try:
			cart = Cart.objects.get(cart_id=_cart_id(request))
		except Cart.DoesNotExist:
			cart = Cart.objects.create(
				cart_id=_cart_id(request)
			)
		cart.save()

		try:
			cart_item = CartItem.objects.get(product=product, cart=cart)
			cart_item.quantity += 1
			cart_item.save()
			return redirect('cart')
		except CartItem.DoesNotExist:
			cart_item = CartItem.objects.create(
				product=product,
				quantity=1,
				cart=cart,
			)
			cart_item.save()
			if request_from == "single_product":
				return redirect(reverse('product_detail', kwargs={"category_slug": category_slug, "product_slug": product_slug, }))
			else:
				return redirect(reverse('products_by_category', kwargs={"category_slug": category_slug}))


def remove_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	if request.user.is_authenticated:
		cart_item = CartItem.objects.get(product=product, user=request.user)
	else:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart')


def remove_cart_item(request, product_id):
	product = Product.objects.get(id=product_id)
	if request.user.is_authenticated:
		cart_item = CartItem.objects.get(product=product, user=request.user)
	else:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart')


def remove_all_cart_items(request):
	if request.user.is_authenticated:
		all_cart_items = CartItem.objects.filter(user=request.user)
	else:
		return redirect('login')
	all_cart_items.delete()


def cart_order_calc(user_is, user_obj, request_1, total, quantity, cart_items):
	shipping = 0
	grand_total = 0
	try:
		if user_is:
			cart_items = CartItem.objects.filter(user=user_obj, is_active=True)
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request_1))
			cart_items = CartItem.objects.filter(cart=cart, is_active=True)
		for cart_item in cart_items:
			total += (round(float(cart_item.product.price), 2) * cart_item.quantity)
			quantity += cart_item.quantity
		shipping = 9.99
		grand_total = total + shipping
	except:
		pass
	return {
		'total': total,
		'quantity': quantity,
		'cart_items': cart_items,
		'shipping': shipping,
		'grand_total': grand_total,
	}


def cart(request, total=0, quantity=0, cart_items=None):
	user_is = request.user.is_authenticated
	user_obj = request.user
	context = cart_order_calc(
		user_is, user_obj, request, total, quantity, cart_items
	)
	return render(request, "shop/cart.html", context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
	user_is = request.user.is_authenticated
	user_obj = request.user
	context = cart_order_calc(
		user_is, user_obj, request, total, quantity, cart_items
	)
	return render(request, "shop/checkout.html", context)


def guide(request):

	params = dict(
		q="Smartphones",
		sortBy="relevancy",
		from_param="2021-08-25",
		apiKey=f"{settings.API_KEY}"
	)

	url = f"https://newsapi.org/v2/everything"

	r = requests.get(url=url, params=params)
	data = r.json()

	articles_list = []
	timestamps = []
	for i in data['articles']:
		date_pub = i['publishedAt']
		timestamps.append(date_pub)
		df = pd.DataFrame({'TIME_STAMP': timestamps})
		df["TIME_STAMP"] = pd.to_datetime(df["TIME_STAMP"])
		df["DATE"] = df["TIME_STAMP"].dt.date
		formatted_dates = df["DATE"]
		article_date = formatted_dates[data['articles'].index(i)]
		article_date = str(article_date)
		articles_list.append({'title': i['title'], 'description': i['description'],
		                     'url': i['url'], 'urlToImage': i['urlToImage'], 'published': article_date})

	return render(request, "shop/guide.html", context={"articles": articles_list})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)

			subject = "Registration successful."
			email_template_name = "password/new_user_greeting.txt"
			c = {
                            "email": user.email,
                            'domain': '127.0.0.1:8000',
                            'site_name': 'MobileShop',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
			}
			email = render_to_string(email_template_name, c)
			try:
				send_mail(subject, email, 'admin@example.com',
				          [user.email], fail_silently=False)
			except BadHeaderError:
				return HttpResponse('Invalid header found.')

			return redirect("/")
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

						cart_products = []
						for item in cart_item:
							products = item.product
							cart_products.append(products)

						cart_item = CartItem.objects.filter(user=user)
						user_products = []
						id = []
						for item in cart_item:
							existing_products = item.product
							user_products.append(existing_products)
							id.append(item.id)

						for pr in cart_products:
							if pr in user_products:
								print("if pr in user_products if block")
								index = user_products.index(pr)
								item_id = id[index]
								item = CartItem.objects.get(id=item_id)
								item.quantity += 1
								item.user = user
								item.save()
							else:
								cart_item = CartItem.objects.filter(cart=cart)
								for item in cart_item:
									item.user = user
									item.save()
				except:
					pass
				login(request, user)
				url = request.META.get('HTTP_REFERER')
				try:
					query = requests.utils.urlparse(url).query
					params = dict(x.split('=') for x in query.split('&'))
					if 'next' in params:
						nextPage = params['next']
						return redirect(nextPage)
				except:
					return redirect("/")
			else:
				pass
		else:
			pass
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login_request.html", context={"login_form": form})


@login_required(login_url='login')
def logout_request(request):
	logout(request)
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
                                            "email": user.email,
                                            'domain': '127.0.0.1:8000',
                                            'site_name': 'MobileShop',
                                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                            "user": user,
                                            'token': default_token_generator.make_token(user),
                                            'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com',
						          [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("/password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form": password_reset_form})


def password_reset_done(request):
	print(f'Request::: {request}')
	return render(request=request, template_name="password/password_reset_done.html")


def place_order(request):
	user = request.user
	subject = "Your order has been placed."
	email_template_name = "shop/place_order.txt"
	c = {
					"email": user.email,
					'domain': '127.0.0.1:8000',
					'site_name': 'MobileShop',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
	}
	email = render_to_string(email_template_name, c)
	try:
		send_mail(subject, email, 'admin@example.com',
					[user.email], fail_silently=False)
	except BadHeaderError:
		return HttpResponse('Invalid header found.')
	remove_all_cart_items(request)
	return render(request=request, template_name="shop/place_order_done.html")