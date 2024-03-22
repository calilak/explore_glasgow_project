from django.shortcuts import render
from django.http import HttpResponse
from app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import *
from .models import Activity, Category

def aboutus(request):
    return render(request,'aboutus.html')

def activities(request):
    return render(request,'activities.html')

def account(request):
    return render(request,'account.html')

def chosenEvent(request):
    return render(request,"chosenEvent.html")

def chosenPlan(request):
    return(request,"chosenPlan.html")

def chosenPlace(request):
    return render(request,"chosenPlace.html")

def events(request):
    events = Event.objects.all().order_by('start_time')  # Get all events, ordered by start time
    return render(request, 'app/events.html', {'events': events})

def learnMore(request):
    return render(request,'learnMore.html')

def index(request):
    return render(request,'app/index.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'app/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('app:index'))
            else:
                return HttpResponse("Your app account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'app/login.html')

@login_required
def restricted(request):
    return render(request, 'app/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('app:index'))

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, 'Your account has been successfully deleted.')
    return redirect('app:index')

def about_us(request):
    team_members = [
        {
            'name': 'Ollie',
            'bio': 'Ollie is a front-end developer with a passion for creating intuitive user interfaces.',
            'image': 'images/profile-pics/ollie.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/olliel1',
            'linkedin_link': 'https://www.linkedin.com/in/ollie-w-livingston',
            'email': 'oliverlivingston@iCloud.com',
        },
        {
            'name': 'Liao',
            'bio': 'Ollie is a front-end developer with a passion for creating intuitive user interfaces.',
            'image': 'images/profile-pics/liao.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/',
            'linkedin_link': '#',
            'email': '#',
        },
        {
            'name': 'Kalila',
            'bio': 'Ollie is a front-end developer with a passion for creating intuitive user interfaces.',
            'image': 'images/profile-pics/kalila.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/',
            'linkedin_link': '#',
            'email': '#',
        },
        {
            'name': 'Matty',
            'bio': 'Ollie is a front-end developer with a passion for creating intuitive user interfaces.',
            'image': 'images/profile-pics/matty.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/',
            'linkedin_link': '#',
            'email': '#',
        },
        {
            'name': 'Oli',
            'bio': 'Ollie is a front-end developer with a passion for creating intuitive user interfaces.',
            'image': 'images/profile-pics/chan.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/',
            'linkedin_link': '#',
            'email': '#',
        },
        # Add other team members in the same way
    ]

    context = {
        'team_members': team_members,
    }

    return render(request, 'app/aboutus.html', context)

def activities(request):
    return render(request, "app/activities.html")

def events(request):
    return render(request, "app/events.html")

def language(request):
    return render(request, "app/language.html")

def map(request):
    return render(request, "app/map.html")

def places(request):
    print("PLaces requested!")
    places_objects = Place.objects.all()
    categories_objects = Category.objects.all()
    tags_objects = Tag.objects.all()

    #List of dictionaries containing all Place object names, categories and tags
    places = [{"name": place.name, "categories": place.categories.all(), 
               "tags": place.tags.all()} for place in places_objects]
    categories = [{"name": category.name} for category in categories_objects]
    tags = [{"name": tag.name} for tag in tags_objects]
    context = {"places": places, "categories": categories, "tags": tags}
    return render(request, "app/places.html", context)

def myPlans(request):
    return render(request, "app/myPlans.html")

def myAccount(request):
    return render(request, "app/myAccount.html")

def privatePolicy(request):
    return render(request, "app/privacyPolicy.html")

def plans(request):
    return render(request, "app/plans.html")

def reviews(request):
    return render(request, "app/reviews.html")

def search_events(request):
    query = request.GET.get('q', '')
    if query:
        events = Event.objects.filter(title__icontains=query).values_list('title', flat=True)[:10]  # Limit to 5 suggestions for efficiency
        suggestions = list(events)
        print (suggestions)
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)

def get_category_activities(category_name):
    
    cat_obj = Category.objecs.get(name=category_name)
    
    activities_objects = Activity.objects.filter(categories=cat_obj)

    activities_list = []
    for activity in activities_objects:
        
        activity_dict = {
            "title": activity.title,
            "description": activity.description,
            "duration": activity.duration,
            "location": activity.location.name if activity.location else None, 
            "categories": [category.name for category in activity.categories.all()],  
            "tags": [tag.name for tag in activity.tags.all()]  
        }
        activities_list.append(activity_dict)

    return activities_list

def get_activities_by_category(request):
    category_name = request.GET.get('category', None)
    
    if category_name:
        category = Category.objects.get(name=category_name)
        activities = Activity.objects.filter(categories=category)
    else:
        activities = Activity.objects.all()

    activities_data = [{
        'title': activity.title,
        'duration': activity.duration,
        'location': activity.location,
    } for activity in activities]

    return JsonResponse({'activities': activities_data})

def add_activity(request):
    if request.method == "POST":
        user = User.objects.first()  # Example: Assign to the first user, replace with your user retrieval logic
        title = request.POST.get('activity-name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        location_name = request.POST.get('location')
        categories_names = request.POST.get('categories').split(',')  # Assuming categories are comma-separated
        tags_names = request.POST.get('tags').split(',')  # Assuming tags are comma-separated

        # You may want to add validation or more complex creation logic here
        location, _ = Place.objects.get_or_create(name=location_name)
        activity = Activity(user=user, title=title, description=description, duration=int(duration), location=location)
        activity.save()
        
        for cat_name in categories_names:
            category, _ = Category.objects.get_or_create(name=cat_name.strip())
            activity.categories.add(category)
        
        for tag_name in tags_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
            activity.tags.add(tag)

        return JsonResponse({"success": True, "message": "Activity added successfully!"})
    
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
