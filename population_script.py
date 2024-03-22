'''
Terminal commands to populate database (delete db.sqlite3 first):
$ python manage.py makemigrations app
$ python manage.py migrate
$ python population_script.py

To create superuser:
$ python manage.py createsuperuser

'''

import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'explore_glasgow.settings')

import django
django.setup()
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from app.models import UserProfile, Category, Tag, Place, Event, Activity, Plan, PlanEvent, PlanActivity, Review

def populate():
    User.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Place.objects.all().delete()
    Event.objects.all().delete()
    Activity.objects.all().delete()
    Plan.objects.all().delete()
    Review.objects.all().delete()
    create_users()
    create_categories_and_tags()
    create_places()
    create_events()
    create_activities()
    create_plans()
    create_reviews()

def create_users():
    users_data = [
        {'username': 'Oli', 'email': 'oli@gmail.com', 'password': 'password'},
        {'username': 'Ollie', 'email': 'ollie@gmail.com', 'password': 'password'},
        {'username': 'Matty', 'email': 'matty@gmail.com', 'password': 'password'},
        {'username': 'Kalila', 'email': 'kalila@gmail.com', 'password': 'password'},
        {'username': 'Liao', 'email': 'liao@gmail.com', 'password': 'password'},
        {'username': 'Max', 'email': 'max@gmail.com', 'password': 'password'},
        {'username': 'Hanna', 'email': 'hanna@gmail.com', 'password': 'password'},
        {'username': 'Lexy', 'email': 'lexy@gmail.com', 'password': 'password'},
        {'username': 'Anna', 'email': 'anna@gmail.com', 'password': 'password'},
        {'username': 'Ivan', 'email': 'ivan@gmail.com', 'password': 'password'},
        {'username': 'Matteo', 'email': 'matteo@gmail.com', 'password': 'password'},
        {'username': 'Nicole', 'email': 'nicole@gmail.com', 'password': 'password'},
        {'username': 'Erin', 'email': 'erin@gmail.com', 'password': 'password'},
        {'username': 'Ruby', 'email': 'ruby@gmail.com', 'password': 'password'},
        {'username': 'Georgie', 'email': 'georgie@gmail.com', 'password': 'password'},
        {'username': 'Mitch', 'email': 'mitch@gmail.com', 'password': 'password'},
        {'username': 'Rob', 'email': 'rob@gmail.com', 'password': 'password'},
        {'username': 'Pat', 'email': 'pat@gmail.com', 'password': 'password'},
        {'username': 'Alex', 'email': 'alex@gmail.com', 'password': 'password'},
        {'username': 'John', 'email': 'john@gmail.com', 'password': 'password'}
    ]

    print("Adding users...")
    for i, user_data in enumerate(users_data):
        user = User.objects.create_user(**user_data)
        if i<5:
            user.is_superuser = True
            user.is_staff = True
            user.save()

    print("Users added successfully!")


def create_categories_and_tags():
    categories_data = ['Personal', 'Fitness', 'Work', 'Education', 'Social', 'Hobbies', 'Restaurant', 'Nightclub', 'Museum', 'Entertainment', 'Shopping']
    tags_data = ['Highly rated', 'Live music', 'Good for large groups', 'Under £20', 'City centre']

    print("Adding categories and tags...")
    for category_name in categories_data:
        Category.objects.get_or_create(name=category_name)

    for tag_name in tags_data:
        Tag.objects.get_or_create(name=tag_name)

    print("Categories and tags added successfully!")

def create_places():
    categories = Category.objects.all()
    tags = Tag.objects.all()
    places_data = [
        {'location': 'ChIJhaMk16FGiEgRQAbI6P-65X8', 'name': 'Paesano Pizza', 'img_ref': 'paesano-pizza.jpg', 'categories': ['Restaurant', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ6WIzTaJGiEgRbfXxsDb9zB8', 'name': 'Shawarma King', 'img_ref': 'shawarma-king.jpg', 'categories': ['Restaurant', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJswdENyZEiEgRhmpBkAxhdrU', 'name': 'Firewater', 'img_ref': 'firewater.jpg', 'categories': ['Nightclub', 'Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated', 'Live music']},
        {'location': 'ChIJ2abQECZEiEgRBwy30iZwok0', 'name': 'Cineworld Cinema', 'img_ref': 'cineworld-cinema.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJM3t6lihEiEgRHgsmDC2DCz0', 'name': 'The Garage', 'img_ref': 'the-garage.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated', 'Live music']},
        {'location': 'ChIJx8oQk6FGiEgRO7odNdW2hXg', 'name': 'Grosvenor Casino', 'img_ref': 'grosvenor-casino.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Highly rated']},
        {'location': 'ChIJ7zFC8tBFiEgRA1AWs9n2fAs', 'name': 'Riverside Museum', 'img_ref': 'riverside-museum.jpg', 'categories': ['Hobbies', 'Education', 'Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ8cF-6MtFiEgRwMvh3DDvPDY', 'name': 'Glasgow Botanic Gardens', 'img_ref': 'botanic-gardens.jpg', 'categories': ['Social', 'Entertainment', 'Hobbies'], 'tags': ['Good for large groups', 'Under £20', 'Highly rated']},
        {'location': 'ChIJi8Q4pSlEiEgRbkvS7hUgqhY', 'name': 'The Bon Accord', 'img_ref': 'the-bon-accord.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJaYl4oCBEiEgRGROD01mT8jo', 'name': 'The Society Room', 'img_ref': 'the-society-room.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJHbP1jvpFiEgRwQl6Mop1zek', 'name': 'Maki & Ramen', 'img_ref': 'maki-and-ramen.jpg', 'categories': ['Restaurant', 'Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJpzaZb6BGiEgRScmAJ9zJgI8', 'name': 'The Ark Glasgow', 'img_ref': 'the-ark.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJjc5Tnp9GiEgRYSkWPUevw6c', 'name': 'Wunderbar', 'img_ref': 'wunderbar.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJdzq8LZ9GiEgRLJ7c2pFX6ik', 'name': 'St. Enoch Centre', 'img_ref': 'st-enoch-centre.jpg', 'categories': ['Social', 'Entertainment', 'Shopping'], 'tags': ['Highly rated']},
        {'location': 'ChIJ3y1BBCBEiEgRD_hQU3qAgNo', 'name': 'Buchanan Galleries', 'img_ref': 'buchanan-galleries.jpg', 'categories': ['Social', 'Entertainment', 'Shopping'], 'tags': ['Highly rated']},
        {'location': 'ChIJIcchPwFHiEgR7DY8Exrxwu0', 'name': 'Vue Cinema Glasgow St. Enoch', 'img_ref': 'vue-cinema.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJtdW_wShEiEgRCy9Sn99Xk3k', 'name': 'Genting Casino Glasgow', 'img_ref': 'genting-casino.jpg', 'categories': ['Social', 'Entertainment'], 'tags': ['Highly rated']},
        {'location': 'ChIJrz4aDSlEiEgRANNqj9MoUQk', 'name': 'The Mitchell Library', 'img_ref': 'mitchell-library.jpg', 'categories': ['Education'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ6ZTla9FFiEgR_p_K8XyyWFI', 'name': 'Kelvingrove Art Gallery and Museum', 'img_ref': 'kelvingrove-museum.jpg', 'categories': ['Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'location': 'ChIJ4d_MFsxFiEgRfvixuazun6c', 'name': 'The Gym Group Glasgow West End', 'img_ref': 'gym-group-west-end.jpg', 'categories': ['Personal', 'Fitness'], 'tags': ['Under £20', 'Highly rated']}
    ]

    print("Adding places...")
    for place_data in places_data:
        tags_list = place_data.pop('tags', [])
        tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_list]
        
        categories_list = place_data.pop('categories', [])
        categories_objs = [Category.objects.get_or_create(name=category_name)[0] for category_name in categories_list]

        place = Place.objects.create(**place_data)

        place.categories.add(*categories_objs)
        place.tags.add(*tags_objs)

    print("Places added successfully!")

def create_events():
    events_data = [
        {'title': 'Fitness Class', 'description': 'Join our fitness class and stay fit!', 'img_ref': 'fitness-class.jpg','start_time': timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 25, 16, 0, 0)), 'location': Place.objects.get(location='ChIJ4d_MFsxFiEgRfvixuazun6c'), 'categories': ['Personal', 'Fitness'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Live Music Night', 'description': 'Join us for a night of live music!','img_ref': 'live-music-night.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 20, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 22, 0, 0)), 'location': Place.objects.get(location='ChIJjc5Tnp9GiEgRYSkWPUevw6c'), 'categories': ['Entertainment', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Movie Night', 'description': 'Enjoy a movie screening under the stars!', 'img_ref': 'movie-night.jpg','start_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 22, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 23, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Entertainment', 'Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Morning Yoga', 'description': 'Start your day right with a nice stretch!','img_ref': 'morning-yoga.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 9, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 10, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Personal', 'Fitness'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Nature Walk', 'description': 'Embrace nature and take a guided tour at Glasgow\'s botanic gardens!','img_ref': 'nature-walk.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 15, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Personal', 'Fitness', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Museum Tour', 'description': 'Learn about glasgow in our museum tour!','img_ref': 'museum-tour.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 14, 30, 0)), 'location': Place.objects.get(location='ChIJ7zFC8tBFiEgRA1AWs9n2fAs'), 'categories': ['Education', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Science Exhibition', 'description': 'Dive into science in our workshop!','img_ref': 'science-exhibition.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 25, 12, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 25, 14, 30, 0)), 'location': Place.objects.get(location='ChIJ7zFC8tBFiEgRA1AWs9n2fAs'), 'categories': ['Education', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Gardening Class', 'description': 'Learn the basics of gardening and grow your own plants!', 'img_ref': 'gardening-class.jpg','start_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 15, 30, 0)), 'location': Place.objects.get(location='ChIJ8cF-6MtFiEgRwMvh3DDvPDY'), 'categories': ['Personal', 'Fitness', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Art Workshop', 'description': 'Learn to create beautiful art at our workshop!','img_ref': 'art-workshop.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 26, 16, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 26, 20, 0, 0)), 'location': Place.objects.get(location='ChIJ6ZTla9FFiEgR_p_K8XyyWFI'), 'categories': ['Education', 'Hobbies'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Food Festival', 'description': 'Explore a variety of cuisines at our food festival!', 'img_ref': 'food-festival.jpg','start_time': timezone.make_aware(datetime.datetime(2024, 3, 24, 12, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 26, 22, 0, 0)), 'location': Place.objects.get(location='ChIJdzq8LZ9GiEgRLJ7c2pFX6ik'), 'categories': ['Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Poker Night', 'description': 'Try your luck at our weekly poker night! Tourney entry £5, one re-buy.', 'img_ref': 'poker-night.jpg','start_time': timezone.make_aware(datetime.datetime(2024, 3, 26, 19, 30, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 26, 23, 0, 0)), 'location': Place.objects.get(location='ChIJi8Q4pSlEiEgRbkvS7hUgqhY'), 'categories': ['Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Chess Night', 'description': 'Come play a game of chess with us! All levels welcome.','img_ref': 'chess-night.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 27, 18, 30, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 27, 22, 0, 0)), 'location': Place.objects.get(location='ChIJi8Q4pSlEiEgRbkvS7hUgqhY'), 'categories': ['Hobbies','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Board Game Night', 'description': 'Come play a game with us!', 'img_ref': 'board-game-night.jpg','start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 18, 30, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 22, 0, 0)), 'location': Place.objects.get(location='ChIJi8Q4pSlEiEgRbkvS7hUgqhY'), 'categories': ['Hobbies','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Comedy Night', 'description': 'Come have a laugh with us!','img_ref': 'comedy-night.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 18, 30, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 22, 0, 0)), 'location': Place.objects.get(location='ChIJaYl4oCBEiEgRGROD01mT8jo'), 'categories': ['Hobbies','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Camden Rocks', 'description': 'Camden Rocks is the quintessential student-club-night. Delivering floor-filler after floor-filler in one of the cities most reputable nights-out.','img_ref': 'camden-rocks.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 17, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 29, 3, 0, 0)), 'location': Place.objects.get(location='ChIJswdENyZEiEgRhmpBkAxhdrU'), 'categories': ['Nightclub','Social'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Language Exchange', 'description': 'Practice speaking different languages with fellow language enthusiasts!','img_ref': 'language-exchange.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 16, 0, 0)), 'location': Place.objects.get(location='ChIJrz4aDSlEiEgRANNqj9MoUQk'), 'categories': ['Hobbies','Social', 'Education'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Group Study Session', 'description': 'Study with fellow students in preparation for exams.','img_ref': 'group-study-session.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 16, 0, 0)), 'location': Place.objects.get(location='ChIJrz4aDSlEiEgRANNqj9MoUQk'), 'categories': ['Social', 'Education'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Tech Hackathon', 'description': '24-hour coding marathon to build innovative tech solutions','img_ref': 'tech-hackathon.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 29, 14, 0, 0)), 'location': Place.objects.get(location='ChIJrz4aDSlEiEgRANNqj9MoUQk'), 'categories': ['Social', 'Education'], 'tags': ['Under £20', 'Highly rated']},
        {'title': 'Book Club Meeting', 'description': 'Join our book club discussion!','img_ref': 'book-club-meeting.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 14, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 16, 0, 0)), 'location': Place.objects.get(location='ChIJpzaZb6BGiEgRScmAJ9zJgI8'), 'categories': ['Social', 'Education', 'Hobbies'], 'tags': ['City centre']},
        {'title': 'Volleyball Social', 'description': 'Come join us after training!','img_ref': 'volleyball-social.jpg', 'start_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 21, 0, 0)), 'end_time': timezone.make_aware(datetime.datetime(2024, 3, 28, 23, 0, 0)), 'location': Place.objects.get(location='ChIJpzaZb6BGiEgRScmAJ9zJgI8'), 'categories': ['Social', 'Entertainment'], 'tags': ['Highly rated']},
    ]

    print("Adding events...")
    for event_data in events_data:
        tags_list = event_data.pop('tags', [])
        tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_list]
        
        categories_list = event_data.pop('categories', [])
        categories_objs = [Category.objects.get_or_create(name=category_name)[0] for category_name in categories_list]

        event = Event.objects.create(**event_data)

        event.categories.add(*categories_objs)
        event.tags.add(*tags_objs)

    print("Events added successfully!")

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
        {'user': users[0], 'title': 'Gardening', 'description': 'Spend time in the garden and nurture your plants.', 'duration': 2, 'location': None, 'categories': ['Hobbies', 'Personal'], 'tags': []},
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

    print("Adding activities...")
    for activity_data in activities_data:
        tags_list = activity_data.pop('tags', [])
        tags_objs = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_list]
        
        categories_list = activity_data.pop('categories', [])
        categories_objs = [Category.objects.get_or_create(name=category_name)[0] for category_name in categories_list]

        activity = Activity.objects.create(**activity_data)

        activity.categories.add(*categories_objs)
        activity.tags.add(*tags_objs)

    print("Activities added successfully!")

def create_plans():
    users = User.objects.all()
    events = Event.objects.all()
    activities = Activity.objects.all()
    plans_data = [
        {'user': users[i], 'title': f"{users[i].username}'s Plan", 'date': events[i].start_time.date(), 'is_public': True} for i in range(20)
    ]

    print("Adding plans...")
    for i, plan_data in enumerate(plans_data):
        plan = Plan.objects.create(**plan_data)

        plan.add_activity(activities[i], events[i].start_time - datetime.timedelta(hours=3)) 

        plan.add_event(events[i])

        plan.save()

    print("Plans added successfully!")

def create_reviews():
    users = User.objects.all()
    places = Place.objects.all()
    plans = Plan.objects.all()
    reviewContent = ['Absolute joke!!','Disgusting!', 'Meh', 'Very good!', 'Amazing!!', 'Overrated af', 'Horrendous', 'Fab!', 'Lovely experience <3', 'Beyond brilliant!', 'Could be better...', 'Underrated spot', 'Ok', 'Appalling', 'Decent!', 'Very interesting!', 'Welcoming and friendly', 'Hard to get to', 'Worth the trip!', 'WOW']
    reviews_data = [
        {'user': users[i], 'content': reviewContent[i], 'rating': (i%5)+1, 'content_type': ContentType.objects.get_for_model(Place), 'object_id': places[j].id} for j in range(20) for i in range(20)
    ] + [
        {'user': users[i], 'content': reviewContent[i], 'rating': (i%5)+1, 'content_type': ContentType.objects.get_for_model(Plan), 'object_id': plans[j].id} for j in range(20) for i in range(20)
    ]

    print("Adding reviews...")
    for review_data in reviews_data:
        Review.objects.create(**review_data)

    print("Reviews added successfully!")

if __name__ == '__main__':
    print('Populating database...')
    populate()
    print('Database populated successfully!')
