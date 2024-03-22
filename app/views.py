from django.shortcuts import get_object_or_404, render
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
from .models import Event
from .models import UserProfile
from .forms import ProfilePictureForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from .models import *
import calendar


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

def chosen_place(request, place_name_slug):
    context_dict = {}
    try:
        # The .get() method returns one model instance or raises an exception.
        chosen_place = Place.objects.get(slug=place_name_slug)
        events = list(Event.objects.filter(location=chosen_place))
        img_dir = "images/places/"
        #CHANGE IMAGE PATH VALUE
        context_dict = {'place': chosen_place, 'image': img_dir+chosen_place.img_ref, 'events': events}
    except Place.DoesNotExist:
        # the template will display the "no place" message for us.
        context_dict['place'] = None
        context_dict['image'] = None
        context_dict['events'] = None
    return render(request,"app/chosen_place.html", context_dict)

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
    context = {"event": event}

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
        events = Event.objects.filter(title__icontains=query).values_list('title', flat=True)[:10]  # Limit to 5 suggestions for efficiency
        suggestions = list(events)
        print (suggestions)
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)