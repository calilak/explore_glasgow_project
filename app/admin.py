from django.contrib import admin
from app.models import UserProfile, Category, Tag, Place, Event, Activity, Plan, PlanEvent, PlanActivity, Review

class PlaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} #admin interface will prepopulate place slugs

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Event)
admin.site.register(Activity)
admin.site.register(Plan)
admin.site.register(PlanEvent)
admin.site.register(PlanActivity)
admin.site.register(Review)