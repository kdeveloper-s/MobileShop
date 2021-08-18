from django.shortcuts import render, redirect
from .models import *
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this


def index(request):
    return render(request, "shop/index.html")


def phones(request):
	mobilephones = MobilePhone.objects.all()
	context = {'phones': mobilephones}
	return render(request, "shop/phones.html", context)


def accessories(request):
    return render(request, "shop/accessories.html")


def guide(request):
    return render(request, "shop/guide.html")


def cart(request):
    return render(request, "shop/cart.html")


def register(request):
    return render(request, "shop/register.html")


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("shop:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="shop/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="shop/login.html", context={"login_form":form})