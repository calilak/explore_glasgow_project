from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the index page of Explore Glasgow.")

def map(request):
    return render(request, "app/map.html")