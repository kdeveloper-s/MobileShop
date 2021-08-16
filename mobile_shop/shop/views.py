from django.shortcuts import HttpResponse, render

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
    
def login(request):
    return render(request, "shop/login.html")
