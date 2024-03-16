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
    path('login/',views.user_login,name='login'),
    path("about-us/", views.about_us, name="about-us"),
    path("activities/", views.activities, name="activities"),
    path("events/", views.events, name="events"),
    path("map/", views.map, name="map"),
    path("places/", views.places, name="places"),
    path('app/', include(('app.urls', 'account'), namespace='app')),
    path('app/', include(('app.urls', 'my-account'), namespace='app')),
    path('app/', include(('app.urls', 'my-plans'), namespace='app')),
    path('app/', include(('app.urls', 'my-plans'), namespace='app')),
    path('app/', include(('app.urls', 'terms-of-use'), namespace='app')),
    path('app/', include(('app.urls', 'private-policy'), namespace='app')),
    path('app/', include(('app.urls', 'learn-more'), namespace='app')),
    path('app/', include(('app.urls', 'chosen-event'), namespace='app')),
    path('app/', include(('app.urls', 'chosen-place'), namespace='app')),
    path('app/', include(('app.urls', 'chosen-plan'), namespace='plan')),
    path('app/', include(('app.urls', 'reviews'), namespace='app')),
    path('app/', include(('app.urls', 'plans'), namespace='app')),
]

#path("", include('app.urls', namespace='app')),