from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseForbidden
from .forms import ProfilePictureForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime,timedelta
from .forms import ReviewForm
import calendar
from .models import Activity, Category

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
    reviews = Review.objects.filter(content_type=ContentType.objects.get_for_model(Plan), object_id=plan.id)
    five_reviews = reviews[:5]  # Get the first 5 reviews for the place
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    num_reviews = reviews.count()
    
    context = {
        'plan': plan,
        'schedule_details': plan.schedule_details,
        'five_reviews': five_reviews,
        'avg_rating': avg_rating,
        'num_reviews': num_reviews
    }
    return render(request, 'app/specificPlan.html', context)


def chosenEvent(request):
    return render(request,"chosenEvent.html")

def chosen_place(request, place_name_slug):
    context_dict = {}
    try:
        # The .get() method returns one model instance or raises an exception.
        chosen_place = Place.objects.get(slug=place_name_slug)
        events = list(Event.objects.filter(location=chosen_place))
        img_dir = "images/places/"
        #CHANGE IMAGE PATH VALUE
        
        reviews = Review.objects.filter(content_type=ContentType.objects.get_for_model(Place), object_id=chosen_place.id)
        five_reviews = reviews[:5]  # Get the first 5 reviews for the place
        avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        num_reviews = reviews.count()

        context_dict = {'place': chosen_place, 'image': img_dir+chosen_place.img_ref, 'events': events, 'five_reviews': five_reviews, 'avg_rating': avg_rating, 'num_reviews': num_reviews}

    except Place.DoesNotExist:
        # the template will display the "no place" message for us.
        context_dict['place'] = None
        context_dict['image'] = None
        context_dict['events'] = None
        context_dict['reviews'] = None 
        context_dict['avg_rating'] = None
        context_dict['num_reviews'] = None

    return render(request,"app/chosen_place.html", context_dict)

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

            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            login(request, new_user)

            return redirect('app:index')

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'app/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
 
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
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('index')
    else:
        return redirect('my_account')

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
    all_events = Event.objects.all()
    tags = Tag.objects.all()
    month_names = [calendar.month_abbr[i] for i in range(1, 13)]
    month = request.GET.get('month')

    if month:
        month_number = month_names.index(month) + 1
        all_events = all_events.filter(date__month=month_number)
    img_dir = "images/events/"
    events = [{"id": event.id,"title": event.title, "image": img_dir+event.img_ref, "location": event.location, "date": event.start_time, "categories": event.categories.all(), "tags": event.tags.all()} for event in all_events]

    context = {
        'events': events,
        'month_names': month_names,
        'tags':tags,
    }
    return render(request, 'app/events.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    img_dir = "images/events/"

    context = {"event": event,
               "image": img_dir+event.img_ref }

    return render(request, "app/event_detail.html", context)

def language(request):
    return render(request, "app/language.html")

def map(request):
    return render(request, "app/map.html")

#changes to make here
def places(request):
    category = request.GET.get('category','') #gets the value of 'category' from the request QueryDict
    places_objects = Place.objects.all()
    categories_objects = Category.objects.all()
    tags_objects = Tag.objects.all()

    if category != "":
        category_places = get_category_places(category)
        places = category_places
        print(places)
    else:
        #List of dictionaries containing all Place object names, categories and tags
        img_dir = "images/places/"
        places = [{"name": place.name, "slug": place.slug, "image": img_dir+place.img_ref, "categories": place.categories.all(), 
                "tags": place.tags.all()} for place in places_objects]
        category_places = places

    print("places:")
    print(place["slug"] for place in places)
    categories = [{"name": category.name} for category in categories_objects]
    tags = [{"name": tag.name} for tag in tags_objects]
    context = {"places": places, "chosen_category_places": category_places, "categories": categories, "tags": tags}

    is_ajax_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax_request:
        #If AJAX request, return JSON response with places HTML content
        places_html = render_to_string('app/places_partial.html', context)
        partial_context = {"places_html": places_html}
        return JsonResponse(partial_context)

    #get all the required HTML content for places.html
    places_html = render_to_string('app/places_partial.html', context)
    context["places_html"] = places_html
    #render the page
    return render(request, 'app/places.html', context)

#get all places of a particular category
def get_category_places(category):
    cat_obj = Category.objects.get(name=category)
    print(cat_obj)
    places_objects = Place.objects.all()

    #List of dictionaries containing all Place object names, categories and tags
    img_dir = "images/places/"
    places_list = []
    for place in places_objects: #go through every place
        if cat_obj in place.categories.all(): #if the required category is one of the place's categories
            places_list.append({"name": place.name, "slug": place.slug, "image": img_dir+place.img_ref,
                                "categories": place.categories.all(), "tags": place.tags.all()})
    
    return places_list
    
def place_reviews(request, place_name_slug):
    place = get_object_or_404(Place, slug=place_name_slug)
    reviews = Review.objects.filter(content_type=ContentType.objects.get_for_model(Place), object_id=place.id)
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    num_reviews = reviews.count()

    context = {
        'place': place,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'num_reviews': num_reviews
    }

    return render(request, 'app/place_reviews.html', context)

def submit_place_review(request, place_name_slug):
    if not request.user.is_authenticated:
        return redirect('app:restricted')
    
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content')
        rating = int(request.POST.get('rating'))
        place = get_object_or_404(Place, slug=place_name_slug)

        # Create the review for the place
        review = Review.objects.create(
            user=user,
            content=content,
            rating=rating,
            content_type=ContentType.objects.get_for_model(Place),
            object_id=place.id
        )

        messages.success(request, 'Your review was submitted successfully!')
        return redirect('app:chosen-place', place_name_slug=place_name_slug)
    else:
        return HttpResponse("Invalid request method", status=400)
    
def plan_reviews(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    reviews = Review.objects.filter(content_type=ContentType.objects.get_for_model(Plan), object_id=plan.id)
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    num_reviews = reviews.count()

    context = {
        'plan': plan,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'num_reviews': num_reviews
    }

    return render(request, 'app/plan_reviews.html', context)

def submit_plan_review(request, plan_id):
    if not request.user.is_authenticated:
        return redirect('app:restricted')
    
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content')
        rating = int(request.POST.get('rating'))
        plan = get_object_or_404(Plan, id=plan_id)

        # Create the review for the plan
        review = Review.objects.create(
            user=user,
            content=content,
            rating=rating,
            content_type=ContentType.objects.get_for_model(Plan),
            object_id=plan.id
        )

        messages.success(request, 'Your review was submitted successfully!')
        return redirect(reverse('app:specific_plan', kwargs={'plan_id': plan_id}))
    else:
        return HttpResponse("Invalid request method", status=400)
    
def myPlans(request):
    return render(request, "app/myPlans.html")

@login_required
def my_account(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    followers_count = user_profile.followers
    public_plans_count = user_profile.public_plans_count
    average_rating = user_profile.average_rating_for_plans
    reviews_count = user_profile.reviews_count_for_plans
    next_plan = Plan.objects.filter(user=user, date__gte=timezone.now()).order_by('date').first()

    star_ratings = range(1, 6)

    if next_plan:
        schedule_details = next_plan.get_schedule()
    else:
        schedule_details = None
        
    context = {
        'user_profile': user_profile,
        'followers_count': followers_count,
        'public_plans_count': public_plans_count,
        'average_rating': average_rating,
        'reviews_count': reviews_count,
        'star_ratings': star_ratings,
        'schedule_details': schedule_details,
    }

    return render(request, 'app/my_account.html', context)

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            picture = form.cleaned_data['picture']
            if picture:
                user_profile.save()
                messages.success(request, 'Profile picture updated successfully.')
                return redirect('my_account')
            else:
                messages.error(request, 'Please select a profile picture.')
    else:
        form = ProfilePictureForm()
    return render(request, 'app/upload_profile_picture.html', {'form': form})

@login_required
@require_POST
def delete_profile_picture(request):
    user_profile = request.user.userprofile
    user_profile.picture.delete()  #delete images
    user_profile.save()
    return redirect('my_account')

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
    return JsonResponse({'events': suggestions}, safe=False)

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
  # Wrap in a dictionary for consistent JSON structure

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