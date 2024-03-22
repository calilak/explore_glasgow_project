from django.shortcuts import render,get_object_or_404
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
from datetime import datetime,timedelta

def aboutus(request):
    return render(request,'aboutus.html')

def activities(request):
    return render(request,'activities.html')

def account(request):
    return render(request,'account.html')

def get_schedule_details(schedule_json):
    schedule_details = []
    for item in schedule_json:
        if item['type'] == 'event':
            event = Event.objects.get(id=item['data'])
            item_detail = {
                'type': 'event',
                'title': event.title,
                'time': event.start_time
            }
        elif item['type'] == 'activity':
            activity = Activity.objects.get(id=item['data'])
            start_time_str = item['start_time']
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            item_detail = {
                'type': 'activity',
                'title': activity.title,
                'time': start_time  # Now a datetime object, consistent with event.start_time
            }
        schedule_details.append(item_detail)
    return schedule_details

def browsePlans(request):
    plans = Plan.objects.all()
    for plan in plans:
        schedule_json = json.loads(plan.schedule)
        plan.schedule_details = get_schedule_details(schedule_json)  # Use the utility function
    context = {
        'plans': plans
    }
    return render(request, 'app/browsePlans.html', context)

def specificPlan(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    schedule_json = json.loads(plan.schedule)
    plan.schedule_details = get_schedule_details(schedule_json)  # Use the utility function
    context = {
        'plan': plan,
        'schedule_details': plan.schedule_details,
    }
    return render(request, 'app/specificPlan.html', context)


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
    top_plans = Plan.objects.all()[:10]  # Adjust this query according to your criteria
    print (top_plans)
    return render(request, 'app/index.html', {'top_plans': top_plans})

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
            'bio': 'Liao is a a university student who is passionate about taking photos to record the scenery.',
            'image': 'images/profile-pics/liao.png', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/anorising_l?igsh=MWZkdzR0cGV6dXdicw%3D%3D&utm_source=qr',
            'linkedin_link': 'https://www.linkedin.com/in/anor-liao-10a938247/',
            'email': 'Anorliao@gmail.com',
        },
        {
            'name': 'Kalila',
            'bio': 'Kalila is a university student who loves going to the best new restaurants in Glasgow.',
            'image': 'images/profile-pics/kalila.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/',
            'linkedin_link': 'https://www.linkedin.com/in/kalila-chand-4a0798243/',
            'email': 'kalilachand@gmail.com',
        },
        {
            'name': 'Matty',
            'bio': 'Matty is a year 2 student at Glasgow University who has a passion for coding.',
            'image': 'images/profile-pics/matty.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/mattyhughes67/',
            'linkedin_link': 'n/a',
            'email': '#2774512h@student.gla.ac.uk',
        },
        {
            'name': 'Oli',
            'bio': 'Oli is a university student who loves exploring Glasgow.',
            'image': 'images/profile-pics/chan.jpg', # Path under your static directory
            'account_link': '#',
            'instagram_link': 'https://www.instagram.com/reviio/',
            'linkedin_link': 'https://www.linkedin.com/in/oliver-chan-b94090226/',
            'email': 'olivercwchan@gmail.com',
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
    print("Places requested!")
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
    query = request.GET.get('q', '')
    if query:
        # Fetch activities by matching titles with the query, limiting to 10 suggestions
        activities = Activity.objects.filter(title__icontains=query).values('id', 'title','duration')[:10]
        activities_data = list(activities)  # Convert QuerySet to list for JSON serialization
    else:
        activities_data = []
    return JsonResponse({'activities': activities_data})

@require_POST
@csrf_exempt
def process_plan(request):
    user = request.user  # Or however you get your user object
    title = request.POST.get('title','')
    date_str = request.POST.get('date', None)
    
    # Default to tomorrow if no date provided
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.now().date() + timedelta(days=1)
        
    event_ids = json.loads(request.POST.get('event_ids', '[]'))
    activities_data = json.loads(request.POST.get('activity_ids', '[{}]'))
    print(activities_data)

    plan = Plan.objects.create(user=user,title=title, date=date)  # Example, adjust accordingly

    # Add events to plan
    for event_id in event_ids:
        event = Event.objects.get(id=event_id)
        plan.add_event(event)

    # Add activities to plan
    for activity_data in activities_data:
        activity = Activity.objects.get(id=activity_data['id'])
        start_time = activity_data['start']
        plan.add_activity(activity, start_time)

    print(plan.schedule)

    return JsonResponse({
        'status': 'success',
        'message': plan.schedule
    })