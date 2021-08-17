from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this

# Create your views here.


def index(request):
    return render(request, "shop/index.html")


def phones(request):
    return render(request, "shop/phones.html")


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
			messages.success(request, "Registration successful.")
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
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login_request.html", context={"login_form": form})


def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("/")
