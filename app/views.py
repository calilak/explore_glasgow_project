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
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from .models import Activity

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('app:index'))  # Adjust to your index page's URL name
        else:
            print(form.errors)
            return HttpResponse("Invalid login details supplied.")
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

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
            'bio': 'Matthew is a second year student at the University of Glasgow.',
            'image': 'images/profile-pics/matty.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/mattyhughes67/',
            'linkedin_link': '#',
            'email': '#2774512@student.gla.ac.uk',
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
        # Fetch events including start and end times
        events = Event.objects.filter(title__icontains=query).values('title', 'start_time', 'end_time','id')[:10]  # Limit to 10 suggestions for efficiency
        suggestions = list(events)
    else:
        suggestions = []
    return JsonResponse({'events': suggestions}, safe=False)  # Wrap in a dictionary for consistent JSON structure

def search_activities(request):
    query = request.GET.get('q', '')  # Note the uppercase GET
    category = request.GET.get('category', '')

    activities_query = Activity.objects.all()

    if query:
        activities_query = activities_query.filter(title__icontains=query)

    if category:
        activities_query = activities_query.filter(category__name=category)
   
    activities = activities_query.values('id', 'title', 'duration')[:10]
    activities_data = list(activities)  # Convert QuerySet to list for JSON serialization
    
    print(activities_data)
    return JsonResponse({'activities': activities_data})

@require_POST
@csrf_exempt  # Only use csrf_exempt for testing purposes or where absolutely necessary
def process_plan(request):
    # Parsing the JSON string from the request
    event_ids = json.loads(request.POST.get('event_ids', '[]'))
    print("Parsed Event IDs:", event_ids)

    
    # Retrieve event titles based on IDs
    event_titles = list(Event.objects.filter(id__in=event_ids).values_list('title', flat=True))
    
    # For testing: Print titles to the Python console
    print("Event Titles:", event_titles)
    
    return JsonResponse({'status': 'success', 'event_titles': event_titles})
     
def user_activities(request):
    activities = Activity.objects.filter(user=request.user) 
    return render(request, 'activitied.html', {'activities':activities})

def add_existing_activity(request):
    activity_name = request.POST.get('activity_name')

    try: 
        activity = Activity.objects.get(title=activity_name)
        
        user_profile = UserProfile.objects.get(user=request.user)
        
        user_profile.activities.add(activity)
        
        return JsonResponse({'success': True})
    
    except Activity.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Activity does not exist.'})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User profile does not exist.'})
    
@require_POST
@csrf_exempt
def add_new_activity(request):
    data = json.loads(request.body)
    user_profile = UserProfile.objects.get(user=request.user)
    title = data.get('title')
    description = data.get('description')
    duration = data.get('duration')
    location_name = data.get('location')
    
    location = Place.objects.get_or_create(name=location_name)[0] if location_name else None
    
    Activity.objects.create(user=user_profile, title=title, description=description, duration=duration, location=location)
    
    return JsonResponse({'status': 'success', 'message': 'Activity added successfully'})





