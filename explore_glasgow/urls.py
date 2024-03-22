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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("app/", include("app.urls")),
    path("admin/", admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('account/my_account/', views.my_account, name='my_account'),
    path('account/upload_profile_picture/', views.upload_profile_picture, name='profile_picture_upload'),
    path("about-us/", views.about_us, name="about-us"),
    path("activities/", views.activities, name="activities"),
    path("events/", views.events, name="events"),
    path("map/", views.map, name="map"),
    path("places/", views.places, name="places"),
    path("browsePlans/",views.browsePlans,name="browsePlans"),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#path("", include('app.urls', namespace='app')),