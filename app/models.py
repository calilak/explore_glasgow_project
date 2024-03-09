import json 

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)
    account_created = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

    @property
    def public_plans_count(self):
        """Returns the count of public plans for the user."""
        return Plan.objects.filter(user=self.user, is_public=True).count()

    @property
    def average_rating_for_plans(self):
        """Calculates the average rating of reviews for the user's plans."""
        plan_content_type = ContentType.objects.get_for_model(Plan)
        reviews = Review.objects.filter(content_type=plan_content_type, object_id__in=self.user.plan_set.all().values_list('id', flat=True))
        return reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def reviews_count_for_plans(self):
        """Returns the count of reviews written for the user's plans."""
        plan_content_type = ContentType.objects.get_for_model(Plan)
        return Review.objects.filter(content_type=plan_content_type, object_id__in=self.user.plan_set.all().values_list('id', flat=True)).count()


# Additional models as provided, with minor adjustments if needed
class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Place(models.Model):
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(Place, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField(default=1)
    location = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name_plural = 'Activities'


    def __str__(self):
        return self.title

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Plan")
    date = models.DateField()
    is_public = models.BooleanField(default=False)
    events = models.ManyToManyField(Event, through='PlanEvent')
    activities = models.ManyToManyField(Activity, through='PlanActivity')
    schedule = models.TextField(default='[]')

    def add_event(self, event):
        schedule = json.loads(self.schedule)
        schedule.append({'type': 'event', 'data': event.id})
        self.schedule = json.dumps(schedule)
        self.save()

    def add_activity(self, activity, start_time):
        schedule = json.loads(self.schedule)
        schedule.append({'type': 'activity', 'data': activity.id, 'start_time': str(start_time)})
        self.schedule = json.dumps(schedule)
        self.save()

    def get_schedule(self):
        schedule_details = []
        for item in self.schedule:
            if item['type'] == 'event':
                event = Event.objects.get(id=item['data'])
                schedule_details.append({'type': 'event', 'data': event})
            elif item['type'] == 'activity':
                activity = Activity.objects.get(id=item['data'])
                start_time = item['start_time']
                schedule_details.append({'type': 'activity', 'data': activity, 'start_time': start_time})
        return schedule_details

    def __str__(self):
        return f"{self.user.username}'s Plan on {self.date}"

class PlanEvent(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class PlanActivity(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Plan activities'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ContentType fields to link Review to either a Place or a Plan
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Review by {self.user.username} - Rating: {self.rating}"
