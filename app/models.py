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
    account_created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username
