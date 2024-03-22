import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from app.models import UserProfile, Category, Tag, Place, Event, Activity, Plan, Review


class UserProfileModelTests(TestCase):
    def test_public_plans_count(self): #tests the method for counting public plans for a newly created user
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(user_profile.public_plans_count, 0)

    def average_rating_for_plans(self): #tests the method for average rating for a newly created user's plans
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(user_profile.average_rating_for_plans, 0)

    def test_reviews_count_for_plans_count(self): #tests the method for counting reviews for a newly created user's plans
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(user_profile.reviews_count_for_plans, 0)

    def test_user_profile_str(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(str(user_profile), 'testuser')

    def test_user_profile_fields(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user, followers=10)
        self.assertEqual(user_profile.user.username, 'testuser')
        self.assertEqual(user_profile.followers, 10)
        self.assertIsNotNone(user_profile.account_created)


class CategoryModelTests(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')

    def test_category_name_field(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(category._meta.get_field('name').max_length, 50)


class TagModelTests(TestCase):
    def test_tag_str(self):
        tag = Tag.objects.create(name='Test Tag')
        self.assertEqual(str(tag), 'Test Tag')

    def test_tag_name_field(self):
        tag = Tag.objects.create(name='Test Tag')
        self.assertEqual(tag._meta.get_field('name').max_length, 50)


class PlaceModelTests(TestCase):
    def test_place_str(self):
        place = Place.objects.create(location='Test Location ID', name='Test Place')
        self.assertEqual(str(place), 'Test Place')

    def test_place_fields(self):
        place = Place.objects.create(location='Test Location ID', name='Test Place')
        self.assertEqual(place.location, 'Test Location ID')
        self.assertEqual(place.name, 'Test Place')

    def test_place_name_field(self):
        place = Place.objects.create(location='Test Location ID', name='Test Place')
        self.assertEqual(place._meta.get_field('name').max_length, 100)
        self.assertEqual(place._meta.get_field('location').max_length, 100)


class EventModelTests(TestCase):
    def test_event_str(self):
        place = Place.objects.create(location='Test Location ID', name='Test Place')
        event = Event.objects.create(title='Test Event', start_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)), end_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 16, 0, 0)), location=place)
        self.assertEqual(str(event), 'Test Event')

    def test_event_fields(self):
        place = Place.objects.create(location='Test Location', name='Test Place')
        event = Event.objects.create(title='Test Event', start_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)), end_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 16, 0, 0)), location=place)
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.location, place)

    def test_event_title_field(self):
        place = Place.objects.create(location='Test Location', name='Test Place')
        event = Event.objects.create(title='Test Event', start_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)), end_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 16, 0, 0)), location=place)
        self.assertEqual(event._meta.get_field('title').max_length, 100)


class ActivityModelTests(TestCase):
    def test_activity_str(self):
        user = User.objects.create(username='testuser')
        activity = Activity.objects.create(user=user, title='Test Activity')
        self.assertEqual(str(activity), 'Test Activity')

    def test_activity_fields(self):
        user = User.objects.create(username='testuser')
        activity = Activity.objects.create(user=user, title='Test Activity')
        self.assertEqual(activity.user.username, 'testuser')
        self.assertEqual(activity.title, 'Test Activity')

    def test_activity_title_field(self):
        user = User.objects.create(username='testuser')
        activity = Activity.objects.create(user=user, title='Test Activity')
        self.assertEqual(activity._meta.get_field('title').max_length, 100)


class PlanModelTests(TestCase):
    def test_plan_str(self):
        user = User.objects.create(username='testuser')
        plan = Plan.objects.create(user=user, date=timezone.make_aware(datetime.datetime(2024, 3, 25)))

        activity = Activity.objects.create(user=user, title='Test Activity')
        plan.add_activity(activity, timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)))

        self.assertEqual(str(plan), "testuser's Plan on 2024-03-25 00:00:00+00:00")

    def test_plan_fields(self):
        user = User.objects.create(username='testuser')
        plan = Plan.objects.create(user=user, date=timezone.make_aware(datetime.datetime(2024, 3, 25)))

        activity = Activity.objects.create(user=user, title='Test Activity')
        plan.add_activity(activity, timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)))

        self.assertEqual(plan.user.username, 'testuser')
        self.assertEqual(plan.date, timezone.make_aware(datetime.datetime(2024, 3, 25)))

    def test_plan_title_field(self):
        user = User.objects.create(username='testuser')
        plan = Plan.objects.create(user=user, date=timezone.make_aware(datetime.datetime(2024, 3, 25)))

        activity = Activity.objects.create(user=user, title='Test Activity')
        plan.add_activity(activity, timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)))
        self.assertEqual(plan._meta.get_field('title').max_length, 100)

    def test_add_activity(self):
        user = User.objects.create(username='testuser')
        plan = Plan.objects.create(user=user, date=timezone.make_aware(datetime.datetime(2024, 3, 25)))

        activity = Activity.objects.create(user=user, title='Test Activity')
        plan.add_activity(activity, timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)))
        self.assertEqual(plan.activities.count(), 1)
        self.assertIn(activity, plan.activities.all())

    def test_add_event(self):
        user = User.objects.create(username='testuser')
        plan = Plan.objects.create(user=user, date=timezone.make_aware(datetime.datetime(2024, 3, 25)))
        place = Place.objects.create(location='Test Location ID', name='Test Place')
        event = Event.objects.create(title='Test Event', start_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)), end_time=timezone.make_aware(datetime.datetime(2024, 3, 25, 16, 0, 0)), location=place)
        
        plan.add_event(event)
        self.assertEqual(plan.events.count(), 1)
        self.assertIn(event, plan.events.all())

    def test_get_schedule(self):
        user = User.objects.create(username='testuser')
        plan = Plan.objects.create(user=user, date=timezone.make_aware(datetime.datetime(2024, 3, 25)))

        activity = Activity.objects.create(user=user, title='Test Activity')
        plan.add_activity(activity, timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)))
        self.assertEqual(plan.get_schedule(), f'[{{"type": "activity", "data": {activity.id}, "start_time": "2024-03-25 14:00:00+00:00"}}]')


class ReviewModelTests(TestCase):
    def test_review_str(self):
        user = User.objects.create(username='testuser')
        place = Place.objects.create(location='Test Location ID', name='Test Place')
        review = Review.objects.create(user=user, content='Test Content', rating=5, content_type=ContentType.objects.get_for_model(Place), object_id=place.id)
        self.assertEqual(str(review), 'Review by testuser - Rating: 5')

    def test_review_fields(self):
        user = User.objects.create(username='testuser')
        place = Place.objects.create(location='Test Location ID', name='Test Place')
        review = Review.objects.create(user=user, content='Test Content', rating=5, content_type=ContentType.objects.get_for_model(Place), object_id=place.id)
        self.assertEqual(review.user.username, 'testuser')
        self.assertEqual(review.content, 'Test Content')
        self.assertEqual(review.rating, 5)

class IndexViewTests(TestCase):
    def test_index_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)

class AboutUsViewTests(TestCase):
    def test_about_us_view(self):
        response = self.client.get(reverse('app:about-us'))
        self.assertEqual(response.status_code, 200)

class MapViewTests(TestCase):
    def test_map_view(self):
        response = self.client.get(reverse('app:map'))
        self.assertEqual(response.status_code, 200)

class ActivityViewTests(TestCase):
    def test_activities_view(self):
        response = self.client.get(reverse('app:activities'))
        self.assertEqual(response.status_code, 200)

class EventViewTests(TestCase):
    def test_events_view(self):
        response = self.client.get(reverse('app:events'))
        self.assertEqual(response.status_code, 200)

class LoginViewTests(TestCase):
    def test_login_view(self):
        #creates a test user
        User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.get(reverse('app:login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('app:login'), {
            'username': 'testuser',
            'password': 'testpassword',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('app:index'))

class RegisterViewTests(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('app:register'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('app:register'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

class PlaceViewTests(TestCase):
    def test_no_places(self):
        response = self.client.get(reverse('app:places'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Places in Glasgow')
        self.assertQuerysetEqual(response.context['places'], [])

    def test_places_exist(self):
        # Create some sample places
        place1 = Place.objects.create(name='Test Place 1', location='Test Location 1 ID', img_ref='st-enoch-centre.jpg') #using st enoch image for this test place
        place2 = Place.objects.create(name='Test Place 2', location='Test Location 2 ID', img_ref='st-enoch-centre.jpg')
        category = Category.objects.get_or_create(name="Test Category")[0]
        tag = Tag.objects.get_or_create(name="Test Tag")[0]
        place1.categories.add(category)
        place1.tags.add(tag)
        place2.categories.add(category)
        place2.tags.add(tag)

        response = self.client.get(reverse('app:places'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Places in Glasgow')
        self.assertContains(response, place1.name)
        self.assertContains(response, place2.name)

        #checks category and tag names are present in the response
        self.assertContains(response, category.name)
        self.assertContains(response, tag.name)