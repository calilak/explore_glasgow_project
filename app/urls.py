from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("home/",views.index,name="index"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("account/", views.account, name="account"),
    path("activities/", views.activities, name="activities"),
    path("events/chosen-event/", views.chosenEvent, name="events_chosen-event"),
    path("events/chosen-place/", views.chosen_place, name="events_chosen-place"),
    path("events/", views.events, name="events"),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path("account/signup/learn-more", views.learnMore, name="account_signup_learn-more"),
    path("account/my-plans/", views.myPlans, name="account_my-plans"),
    path("account/my_account/", views.my_account, name="my_account"),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('account/upload_profile_picture/', views.upload_profile_picture, name='profile_picture_upload'),
    path('account/profile_picture_delete/', views.delete_profile_picture, name='profile_picture_delete'),
    path("places/", views.places, name="places"),
    path("places/<slug:place_name_slug>/", views.chosen_place, name="chosen-place"), #mapping a place url to the chosen_place view
    path('places/<slug:place_name_slug>/reviews/', views.place_reviews, name='place_reviews'), #reviews for each chosen place
    path('places/<slug:place_name_slug>/submit-review/', views.submit_place_review, name='submit_place_review'), #used for the view to submit review for place
    path("places/<str:category>/", views.places, name="places"),
    path("account/signup/private-policy", views.privatePolicy, name="account_signup_private-policy"),
    path("account/signup/", views.register, name="account_signup"),
    path("account/signup/terms-of-use", views.register, name="account_signup_terms-of-use"),
    path("plans/", views.plans, name="plans"),
    path("plans/<int:plan_id>/reviews/", views.plan_reviews, name="plan_reviews"),
    path("plans/<int:plan_id>/submit-review/", views.submit_plan_review, name='submit_plan_review'),
    path("account/my-plans/chosen-plan/", views.specificPlan, name="account_my-plans_chosen-plan"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path("about-us/", views.about_us, name="about-us"),
    path("activities/", views.activities, name="activities"),
    path("events/", views.events, name="events"),
    path("language/", views.language, name="language"),
    path("map/", views.map, name="map"),
    path("search-events/",views.search_events,name="search-events"),
    path('search-activities/', views.search_activities, name='search-activities'),
    path("process-plans/",views.process_plan,name="process-plans"),
    path("browsePlans/",views.browsePlans,name="browsePlans"),
    path('plans/<int:plan_id>/', views.specificPlan, name='specific_plan'),
    path("activities/",views.get_category_activities,name='get_category_activities'),
    path('activities/', views.get_activities_by_category, name='get_activities_by_category'),
    path('activities/', views.add_activity, name='add_activity')
]