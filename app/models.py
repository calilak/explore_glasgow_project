from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# ollie working on this
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    followers = models.IntegerField(default=0)
    # count of public plans
    # average stars calculated
    # count of reviews
    account_created = models.DateTimeField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username
    
# category and tags models
class Category(models.Model):
    name = models.CharField(max_length=50)

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0) # Assuming rating is an integer from 0 to 5 or something similar
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Place(models.Model):
    location = models.CharField(max_length=100) # this will take a google api place id which is a unique string
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    review = models.ForeignKey(Review,on_delete=models.CASCADE)

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(Place, on_delete=models.CASCADE) 
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # if superuser then it is a default activity - for all users to see
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField(default=1)
    location = models.ForeignKey(Place, on_delete=models.CASCADE) 
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_public = models.BooleanField(default=False)
    events = models.ManyToManyField(Event, through='PlanEvent')
    activities = models.ManyToManyField(Activity,through='PlanActivity')
    review = models.ForeignKey(Review,on_delete=models.CASCADE)

class PlanEvent(models.Model): # this is the intermediary between a users plan and event so that multiple users can add the same event to their plans
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class PlanActivity(models.Model): # this is the intermediary between a users plan and event so that multiple users can add the same event to their plans
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

# ----------------------------------------------------------------------------


