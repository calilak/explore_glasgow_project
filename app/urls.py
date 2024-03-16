from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("home/",views.index,name="index"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("account/", views.account, name="account"),
    path("activities/", views.activities, name="activities"),
    path("events/chosen-event/", views.chosenEvent, name="events_chosen-event"),
    path("events/chosen-place/", views.chosenPlace, name="events_chosen-place"),
    path("events/", views.events, name="events"),
    path("account/signup/learn-more", views.learnMore, name="account_signup_learn-more"),
    path("account/my-plans/", views.myPlans, name="account_my-plans"),
    path("account/my-account/", views.myAccount, name="account_my-account"),
    path("places/", views.places, name="places"),
    path("account/signup/private-policy", views.privatePolicy, name="account_signup_private-policy"),
    path("account/signup/", views.register, name="account_signup"),
    path("account/signup/terms-of-use", views.register, name="account_signup_terms-of-use"),
    path("plans/", views.plans, name="plans"),
    path("plans/chosen-plan", views.chosenPlan, name="chosen-plan"),
    path("plans/chosen-plan/reviews/", views.reviews, name="reviews"),
    path("plans/chosen-place/reviews/", views.reviews, name="reviews"),
    path("account/my-plans/chosen-plan/", views.chosenPlan, name="account_my-plans_chosen-plan"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path("about-us/", views.about_us, name="about-us"),
    path("activities/", views.activities, name="activities"),
    path("events/", views.events, name="events"),
    path("map/", views.map, name="map"),
    path("search-events/",views.search_events,name="search-events"),
    path('search-activities/', views.search_activities, name='search-activities'),
    path("process-plans/",views.process_plan,name="process-plans"),
]