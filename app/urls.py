from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("aboutus/", views.aboutus, name="aboutus"),
    path("account/", views.account, name="account"),
    path("activities/", views.activities, name="activities"),
    path("events/chosen-event/", views.chosenEvent, name="events_chosen-event"),
    path("events/chosen-place/", views.chosenPlace, name="events_chosen-place"),
    path("events/", views.events, name="events"),
    path("account/signup/learn-more", views.learnMore, name="account_signup_learn-more"),
    path("maps", views.maps, name="maps"),
    path("account/my-plans/", views.myPlans, name="account_my-plans"),
    path("account/my-account/", views.myAccount, name="account_my-account"),
    path("places/", views.places, name="places"),
    path("account/signup/private-policy", views.privatePolicy, name="account_signup_private-policy"),
    path("account/signup/", views.signup, name="account_signup"),
    path("account/signup/terms-of-use", views.signup, name="account_signup_terms-of-use"),
    path("plans/", views.plans, name="plans"),
    path("plans/chosen-plan", views.chosenPlan, name="chosen-plan"),
    path("plans/chosen-plan/reviews/", views.reviews, name="reviews"),
    path("plans/chosen-place/reviews/", views.reviews, name="reviews"),
    path("account/my-plans/chosen-plan/", views.chosenPlan, name="account_my-plans_chosen-plan"),




    
]