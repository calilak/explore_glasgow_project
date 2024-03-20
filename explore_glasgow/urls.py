"""
URL configuration for explore_glasgow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# ollies branch
from django.contrib import admin
from django.urls import include, path
from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("app/", include("app.urls")),
    path("admin/", admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path("about-us/", views.about_us, name="about-us"),
    path("activities/", views.activities, name="activities"),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path("language/", views.language, name="language"),
    path("map/", views.map, name="map"),
    path("places/", views.places, name="places"),
    path('app/account/', include(('app.urls', 'app_account'), namespace='app_account')),
    path('app/my-account/', include(('app.urls', 'app_my_account'), namespace='app_my_account')),
    path('app/my-plans/', include(('app.urls', 'app_my_plans'), namespace='app_my_plans')),
    path('app/terms-of-use/', include(('app.urls', 'app_terms_of_use'), namespace='app_terms_of_use')),
    path('app/private-policy/', include(('app.urls', 'app_private_policy'), namespace='app_private_policy')),
    path('app/learn-more/', include(('app.urls', 'app_learn_more'), namespace='app_learn_more')),
    path('app/chosen-event/', include(('app.urls', 'app_chosen_event'), namespace='app_chosen_event')),
    path('app/chosen-place/', include(('app.urls', 'app_chosen_place'), namespace='app_chosen_place')),
    path('app/chosen-plan/', include(('app.urls', 'app_chosen_plan'), namespace='app_chosen_plan')),
    path('app/reviews/', include(('app.urls', 'app_reviews'), namespace='app_reviews')),
    path('app/plans/', include(('app.urls', 'app_plans'), namespace='app_plans')),
]

#path("", include('app.urls', namespace='app')),