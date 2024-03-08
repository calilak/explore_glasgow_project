from django.shortcuts import render
from django.http import HttpResponse

def aboutus(request):
    return render(request,'aboutus.html')

def activities(request):
    return render(request,'activities.html')

def account(request):
    return render(request,'account.html')

def chosenEvent(request):
    return render(request,"chosenEvent.html")

def chosenPlan(request):
    return(request,"chosenPlan.html")

def chosenPlace(request):
    return render(request,"chosenPlace.html")

def events(request):
    return render(request,'events.html')

def learnMore(request):
    return render(request,'learnMore.html')

def index(request):
    return render(request,'index.html')

def maps(request):
    return render(request,'maps.html')

def myPlans(request):
    return render(request,"myPlans.html")

def myAccount(request):
    return render(request,"myAccount.html")

def places(request):
    return render(request,'places.html')

def plans(request):
    return(request,"plans.html")

def privatePolicy(request):
    return render(request,"privatePolicy.html")

def reviews(request):
    return render(request,"reviews.html")
    
def signup(request):
    return render(request,"signup.html")

def termsOfUse(request):
    return render(request,"termsOfUse.html")
