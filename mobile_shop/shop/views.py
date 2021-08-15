from django.shortcuts import HttpResponse, render

# Create your views here.
def index(request):
    return render(request, "shop/index.html")

def phones(request):
    return render(request, "shop/phones.html")
