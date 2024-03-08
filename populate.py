import os
import datetime
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'explore_glasgow.settings')

import django
django.setup()
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from app.models import UserProfile, Category, Tag, Place, Event, Activity, Plan, PlanEvent, PlanActivity, Review

def populate():
    create_users()
    create_categories_and_tags()
    create_places()
    create_events()
    create_activities()
    create_plans()
    create_reviews()

def create_users():
    users_data = [
        {'username': 'Oli', 'email': 'user1@example.com', 'password': 'password'},
        {'username': 'Ollie', 'email': 'user2@example.com', 'password': 'password'},
        {'username': 'Matty', 'email': 'user3@example.com', 'password': 'password'},
        {'username': 'Kalila', 'email': 'user4@example.com', 'password': 'password'},
        {'username': 'Liao', 'email': 'user5@example.com', 'password': 'password'},
        {'username': 'Max', 'email': 'user6@example.com', 'password': 'password'},
        {'username': 'Hanna', 'email': 'user7@example.com', 'password': 'password'},
        {'username': 'Lexy', 'email': 'user8@example.com', 'password': 'password'},
        {'username': 'Anna', 'email': 'user9@example.com', 'password': 'password'},
        {'username': 'Ivan', 'email': 'user10@example.com', 'password': 'password'},
        {'username': 'Matteo', 'email': 'user11@example.com', 'password': 'password'},
        {'username': 'Nicole', 'email': 'user12@example.com', 'password': 'password'},
        {'username': 'Pepper', 'email': 'user13@example.com', 'password': 'password'},
        {'username': 'Ruby', 'email': 'user14@example.com', 'password': 'password'},
        {'username': 'Georgie', 'email': 'user15@example.com', 'password': 'password'},
        {'username': 'Mitch', 'email': 'user16@example.com', 'password': 'password'},
        {'username': 'Rob', 'email': 'user17@example.com', 'password': 'password'},
        {'username': 'Pat', 'email': 'user18@example.com', 'password': 'password'},
        {'username': 'Alex', 'email': 'user19@example.com', 'password': 'password'},
        {'username': 'John', 'email': 'user20@example.com', 'password': 'password'}
    ]
    for user_data in users_data:
        User.objects.create_user(**user_data)

def create_categories_and_tags():
    categories_data = ['Personal', 'Fitness', 'Work', 'Education', 'Social', 'Hobbies', 'Restaurant', 'Nightclub', 'Museum', 'Entertainment', 'Shopping']
    tags_data = ['Highly rated', 'Live music', 'Good for large groups', 'Under £20', 'City centre']

    for category_name in categories_data:
        Category.objects.get_or_create(name=category_name)

    for tag_name in tags_data:
        Tag.objects.get_or_create(name=tag_name)

def create_places():
    categories = Category.objects.all()
    tags = Tag.objects.all()
    places_data = [
        {'location': 'ChIJhaMk16FGiEgRQAbI6P-65X8', 'name': 'Paesano Pizza', 'categories': ['Restaurant', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ6WIzTaJGiEgRbfXxsDb9zB8', 'name': 'Shawarma King', 'categories': ['Restaurant', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJswdENyZEiEgRhmpBkAxhdrU', 'name': 'Firewater', 'categories': ['Nightclub', 'Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated', 'Live music']},
        {'location': 'ChIJ2abQECZEiEgRBwy30iZwok0', 'name': 'Cineworld Cinema', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJM3t6lihEiEgRHgsmDC2DCz0', 'name': 'The Garage', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated', 'Live music']},
        {'location': 'ChIJx8oQk6FGiEgRO7odNdW2hXg', 'name': 'Grosvenor Casino', 'categories': ['Social', 'Entertainment'], 'tags': ['Highly rated']},
        {'location': 'ChIJ7zFC8tBFiEgRA1AWs9n2fAs', 'name': 'Riverside Museum', 'categories': ['Hobbies', 'Education', 'Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ8cF-6MtFiEgRwMvh3DDvPDY', 'name': 'Glasgow Botanic Gardens', 'categories': ['Social', 'Entertainment', 'Hobbies'], 'tags': ['Good for large groups', 'Under £20', 'Highly rated']},
        {'location': 'ChIJi8Q4pSlEiEgRbkvS7hUgqhY', 'name': 'The Bon Accord', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJaYl4oCBEiEgRGROD01mT8jo', 'name': 'The Society Room', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJHbP1jvpFiEgRwQl6Mop1zek', 'name': 'Maki & Ramen', 'categories': ['Restaurant', 'Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJpzaZb6BGiEgRScmAJ9zJgI8', 'name': 'The Ark Glasgow', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJjc5Tnp9GiEgRYSkWPUevw6c', 'name': 'Wunderbar', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJdzq8LZ9GiEgRLJ7c2pFX6ik', 'name': 'St. Enoch Centre', 'categories': ['Social', 'Entertainment', 'Shopping'], 'tags': ['Highly rated']},
        {'location': 'ChIJ3y1BBCBEiEgRD_hQU3qAgNo', 'name': 'Buchanan Galleries', 'categories': ['Social', 'Entertainment', 'Shopping'], 'tags': ['Highly rated']},
        {'location': 'ChIJIcchPwFHiEgR7DY8Exrxwu0', 'name': 'Vue Cinema Glasgow St. Enoch', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJtdW_wShEiEgRCy9Sn99Xk3k', 'name': 'Genting Casino Glasgow', 'categories': ['Social', 'Entertainment'], 'tags': ['Highly rated']},
        {'location': 'ChIJrz4aDSlEiEgRANNqj9MoUQk', 'name': 'The Mitchell Library', 'categories': ['Education'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ6ZTla9FFiEgR_p_K8XyyWFI', 'name': 'Kelvingrove Art Gallery and Museum', 'categories': ['Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ4d_MFsxFiEgRfvixuazun6c', 'name': 'The Gym Group Glasgow West End', 'categories': ['Personal', 'Fitness'], 'tags': ['Under £20', 'Highly rated']}
    ]

    for place_data in places_data:
        tags_list = place_data.pop('tags', [])
        tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_list]
        
        categories_list = place_data.pop('categories', [])
        categories_objs = [Category.objects.get_or_create(name=category_name)[0] for category_name in categories_list]

        place = Place.objects.create(**place_data)

        place.categories.add(*categories_objs)
        place.tags.add(*tags_objs)

def create_events():
    events_data = [
        {'title': 'Fitness Class', 'description': 'Join our fitness class and stay fit!', 'start_time': timezone.make_aware(datetime(2024, 3, 25, 14, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 25, 16, 0, 0)), 'location': Place.objects.get(location='ChIJ4d_MFsxFiEgRfvixuazun6c'), 'categories': ['Personal', 'Fitness'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Live Music Night', 'description': 'Join us for a night of live music!', 'start_time': timezone.make_aware(datetime(2024, 3, 24, 20, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 24, 22, 0, 0)), 'location': Place.objects.get(location='ChIJjc5Tnp9GiEgRYSkWPUevw6c'), 'categories': ['Entertainment', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Movie Night', 'description': 'Enjoy a movie screening under the stars!', 'start_time': timezone.make_aware(datetime(2024, 3, 24, 22, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 24, 23, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Entertainment', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Morning Yoga', 'description': 'Start your day right with a nice stretch!', 'start_time': timezone.make_aware(datetime(2024, 3, 24, 9, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 24, 10, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Personal', 'Fitness'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Nature Walk', 'description': 'Embrace nature and take a guided tour at Glasgow\'s botanic gardens!', 'start_time': timezone.make_aware(datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 24, 15, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Personal', 'Fitness', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Museum Tour', 'description': 'Learn about glasgow in our museum tour!', 'start_time': timezone.make_aware(datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 24, 14, 30, 0)), 'location': Place.objects.get(location='ChIJ7zFC8tBFiEgRA1AWs9n2fAs'), 'categories': ['Education', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Science Exhibition', 'description': 'Dive into science in our workshop!', 'start_time': timezone.make_aware(datetime(2024, 3, 25, 12, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 25, 14, 30, 0)), 'location': Place.objects.get(location='ChIJ7zFC8tBFiEgRA1AWs9n2fAs'), 'categories': ['Education', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Gardening Class', 'description': 'Learn the basics of gardening and grow your own plants!', 'start_time': timezone.make_aware(datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 24, 15, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Personal', 'Fitness', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Art Workshop', 'description': 'Learn to create beautiful art at our workshop!', 'start_time': timezone.make_aware(datetime(2024, 3, 26, 16, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 26, 20, 0, 0)), 'location': Place.objects.get(location='ChIJ6ZTla9FFiEgR_p_K8XyyWFI'), 'categories': ['Education', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Food Festival', 'description': 'Explore a variety of cuisines at our food festival!', 'start_time': timezone.make_aware(datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 26, 22, 0, 0)), 'location': Place.objects.get(location='ChIJdzq8LZ9GiEgRLJ7c2pFX6ik'), 'categories': ['Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Poker Night', 'description': 'Try your luck at our weekly poker night! Tourney entry £5, one re-buy.', 'start_time': timezone.make_aware(datetime(2024, 3, 26, 19, 30, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 26, 23, 0, 0)), 'location': Place.objects.get(location='ChIJi8Q4pSlEiEgRbkvS7hUgqhY'), 'categories': ['Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Chess Night', 'description': 'Come play a game of chess with us! All levels welcome.', 'start_time': timezone.make_aware(datetime(2024, 3, 27, 18, 30, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 27, 22, 0, 0)), 'location': Place.objects.get(location='ChIJi8Q4pSlEiEgRbkvS7hUgqhY'), 'categories': ['Hobbies','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Board Game Night', 'description': 'Come play a game with us!', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 18, 30, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 28, 22, 0, 0)), 'location': Place.objects.get(location='ChIJi8Q4pSlEiEgRbkvS7hUgqhY'), 'categories': ['Hobbies','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Comedy Night', 'description': 'Come have a laugh with us!', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 18, 30, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 28, 22, 0, 0)), 'location': Place.objects.get(location='ChIJaYl4oCBEiEgRGROD01mT8jo'), 'categories': ['Hobbies','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Camden Rocks', 'description': 'Camden Rocks is the quintessential student-club-night. Delivering floor-filler after floor-filler in one of the cities most reputable nights-out.', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 17, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 29, 3, 0, 0)), 'location': Place.objects.get(location='ChIJswdENyZEiEgRhmpBkAxhdrU'), 'categories': ['Nightclub','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Language Exchange', 'description': 'Practice speaking different languages with fellow language enthusiasts!', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 28, 16, 0, 0)), 'location': Place.objects.get(location='ChIJrz4aDSlEiEgRANNqj9MoUQk'), 'categories': ['Hobbies','Social', 'Education'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Group Study Session', 'description': 'Study with fellow students in preparation for exams.', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 28, 16, 0, 0)), 'location': Place.objects.get(location='ChIJrz4aDSlEiEgRANNqj9MoUQk'), 'categories': ['Social', 'Education'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Tech Hackathon', 'description': '24-hour coding marathon to build innovative tech solutions', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 29, 14, 0, 0)), 'location': Place.objects.get(location='ChIJrz4aDSlEiEgRANNqj9MoUQk'), 'categories': ['Social', 'Education'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Book Club Meeting', 'description': 'Join our book club discussion!', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 28, 16, 0, 0)), 'location': Place.objects.get(location='ChIJpzaZb6BGiEgRScmAJ9zJgI8'), 'categories': ['Social', 'Education', 'Hobbies'], 'tags': ['City centre']},
        {'title': 'Volleyball Social', 'description': 'Come join us after training!', 'start_time': timezone.make_aware(datetime(2024, 3, 28, 21, 0, 0)), 'end_time': timezone.make_aware(datetime(2024, 3, 28, 23, 0, 0)), 'location': Place.objects.get(location='ChIJpzaZb6BGiEgRScmAJ9zJgI8'), 'categories': ['Social', 'Entertainment'], 'tags': ['Highly rated']},
    ]
    for event_data in events_data:
        tags_list = event_data.pop('tags', [])
        tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_list]
        1
        categories_list = event_data.pop('categories', [])
        categories_objs = [Category.objects.get_or_create(name=category_name)[0] for category_name in categories_list]

        event = Event.objects.create(**event_data)

        event.categories.add(*categories_objs)
        event.tags.add(*tags_objs)

def create_activities():
    users = User.objects.all()
    activities_data = [
        {'user': users[0], 'title': 'Painting', 'description': 'Create beautiful art with colors.', 'duration': 2, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Chess', 'description': 'Exercise your mind with a game of chess.', 'duration': 2, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Gym', 'description': 'Weight training and cardio', 'duration': 1, 'location': Place.objects.get(location='ChIJ4d_MFsxFiEgRfvixuazun6c'), 'categories': ['Personal', 'Fitness', 'Hobbies'], 'tags': []},
        {'user': users[0], 'title': 'Meditation', 'description': 'Relax and reflect, take a break from your troubles.', 'duration': 1, 'location': None, 'categories': ['Personal'], 'tags': []},
        {'user': users[0], 'title': 'Coding Practice', 'description': 'Improve your coding skills with some practice.', 'duration': 2, 'location': None, 'categories': ['Work', 'Education'], 'tags': []},
        {'user': users[0], 'title': 'Reading', 'description': 'Dive into a good book.', 'duration': 2, 'location': None, 'categories': ['Personal', 'Education', 'Hobbies'], 'tags': []},
        {'user': users[0], 'title': 'Yoga Session', 'description': 'Relax and rejuvenate with a yoga session.', 'duration': 1, 'location': None, 'categories': ['Fitness', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Drawing', 'description': 'Unleash your creativity through drawing.', 'duration': 2, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Language Learning', 'description': 'Learn a new language.', 'duration': 2, 'location': None, 'categories': ['Education', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Gardening', 'description': 'Spend time in the garden and nurture your plants.', 'duration': 3, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Music Practice', 'description': 'Practice playing a musical instrument.', 'duration': 2, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Photography', 'description': 'Capture moments through photography.', 'duration': 2, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Running', 'description': 'Go for a run and stay fit.', 'duration': 1, 'location': None, 'categories': ['Fitness', 'Hobbies'], 'tags': []},
        {'user': users[0], 'title': 'Tennis', 'description': 'Play some tennis with your friends and keep fit.', 'duration': 1, 'location': None, 'categories': ['Fitness', 'Hobbies', 'Social'], 'tags': []},
        {'user': users[0], 'title': 'Volleyball', 'description': 'Play volleyball with your friends', 'duration': 1, 'location': None, 'categories': ['Fitness', 'Hobbies', 'Social'], 'tags': []},
        {'user': users[0], 'title': 'Writing', 'description': 'Express yourself through writing.', 'duration': 2, 'location': None, 'categories': ['Personal', 'Hobbies'], 'tags': []},
        {'user': users[0], 'title': 'Volunteering', 'description': 'Give back to the community through volunteering.', 'duration': 3, 'location': None, 'categories': ['Social'], 'tags': []},
        {'user': users[0], 'title': 'Board Games', 'description': 'Have fun with friends playing board games.', 'duration': 2, 'location': None, 'categories': ['Social', 'Hobbies'], 'tags': []},
        {'user': users[0], 'title': 'Cooking', 'description': 'Make some nice food for yourself. Yum!', 'duration': 2, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
        {'user': users[0], 'title': 'Film Night', 'description': 'Enjoy a movie night at home.', 'duration': 2, 'location': None, 'categories': ['Personal', 'Entertainment'], 'tags': []}
    ]

    for activity_data in activities_data:
        tags_list = activity_data.pop('tags', [])
        tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_list]
        
        categories_list = activity_data.pop('categories', [])
        categories_objs = [Category.objects.get_or_create(name=category_name)[0] for category_name in categories_list]

        activity = Activity.objects.create(**activity_data)

        activity.categories.add(*categories_objs)
        activity.tags.add(*tags_objs)

def create_plans():
    users = User.objects.all()
    events = Event.objects.all()
    activities = Activity.objects.all()
    plans_data = [
        {'user': users[0], 'title': f"{users[0].username}'s Plan", 'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[1], 'title': f"{users[1].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[2], 'title': f"{users[2].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[3], 'title': f"{users[3].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[4], 'title': f"{users[4].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[5], 'title': f"{users[5].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[6], 'title': f"{users[6].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[7], 'title': f"{users[7].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[8], 'title': f"{users[8].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[9], 'title': f"{users[9].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[10], 'title': f"{users[10].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[11], 'title': f"{users[11].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': False},
        {'user': users[12], 'title': f"{users[12].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': False},
        {'user': users[13], 'title': f"{users[13].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': False},
        {'user': users[14], 'title': f"{users[14].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': False},
        {'user': users[15], 'title': f"{users[5].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[16], 'title': f"{users[6].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[17], 'title': f"{users[7].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[18], 'title': f"{users[8].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True},
        {'user': users[19], 'title': f"{users[9].username}'s Plan",'date': timezone.make_aware(datetime(2024, 3, 25)), 'is_public': True}
    ]

    for plan_data in plans_data:
        plan = Plan.objects.create(**plan_data)

        plan.add_event(events[0]) #adds the first event to everyones plan

        plan.add_activity(activities[random.randrange(20)], timezone.make_aware(datetime(2024, 3, 25, 17, 0, 0))) 
        plan.add_activity(activities[random.randrange(20)], timezone.make_aware(datetime(2024, 3, 25, 21, 0, 0)))  

        plan.save()

def create_reviews():
    users = User.objects.all()
    reviews_data = [
        {'user': users[i], 'content': random.choice(['Amazing stuff!','Very good!', 'Great service!', 'Shocking wait time...', 'Rude staff!', 'Ok food.']), 'rating': random.randrange(1,6), 'content_type': ContentType.objects.get_for_model(Place), 'object_id': Place.objects.first().id} for i in range(20)
    ]
    for review_data in reviews_data:
        Review.objects.create(**review_data)

if __name__ == '__main__':
    print('Populating database...')
    populate()
    print('Database populated successfully!')