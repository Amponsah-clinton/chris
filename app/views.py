from django.shortcuts import render, redirect, get_object_or_404
from .forms import contactform, PostProfileForm, CategoryForm, ReportProfileForm
from . models import PostProfile, Category



def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to a list view of categories
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})




def index(request):
    categories = Category.objects.all()[:4]
    categories_with_count = []
    for category in categories:
        post_count = PostProfile.objects.filter(category=category).count()
        categories_with_count.append({
            'category': category,
            'post_count': post_count
        })

    featured_profiles = PostProfile.objects.filter(is_approved=True)[:5]
    fresh_vacancies = Vacancy.objects.filter(is_approved=True, deadline__gte=timezone.now()).order_by('-date_posted')[:4]
    context = {
        'categories_with_count': categories_with_count,
        'featured_profiles': featured_profiles,
        'fresh_vacancies': fresh_vacancies
    }
    return render(request, 'index.html', context)




def search_results(request):
    query = request.GET.get('q')
    context = {
        'query': query,
    }
    return render(request, 'search_results.html', context)

from django.db.models import Q

def search_results(request):
    query = request.GET.get('q')
    
    if query:
        search_results = Vacancy.objects.filter(Q(title__icontains=query) | Q(location__icontains=query)| Q(regions__icontains=query))
    else:
        search_results = []

    context = {
        'query': query,
        'search_results': search_results,
    }
    return render(request, 'search_results.html', context)


def contact(request):
    form = contactform()
    if request.method=='POST':
        form = contactform(request.POST)
        if form.is_valid():
          form.save()
          form = contactform()
    return render(request, 'contact.html')


def all_categories(request):
    categories = Category.objects.all()

    categories_with_count = [] 
    for category in categories:
        post_count = category.postprofile_set.count() 
        categories_with_count.append({'category': category, 'post_count': post_count})
    context = {
        'categories_with_count': categories_with_count
    }
    return render(request, 'all_categories.html', context)

import os

def create_post_profile(request):
    if request.method == 'POST':
        form = PostProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.save()  # Save the main PostProfile instance

            uploaded_images = request.FILES.getlist('sample_works')
            image_paths = []

            base_dir = os.path.join('media', 'sample_works', str(new_post.id))
            os.makedirs(base_dir, exist_ok=True)

            for image in uploaded_images:
                image_name = os.path.join(base_dir, image.name)
                image_paths.append(image_name)
                with open(image_name, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            new_post.sample_works = ', '.join(image_paths)  # Join image paths as a single string
            new_post.save()

            return redirect('profile_list')
    else:
        form = PostProfileForm()

    return render(request, 'create_post_profile.html', {'form': form})



from django.shortcuts import render
from .models import PostProfile

def profile_list(request):
    location_query = request.GET.get('location')
    title_query = request.GET.get('title')
    region_query = request.GET.get('region')
    profiles = PostProfile.objects.all()
    if location_query:
        profiles = profiles.filter(location__icontains=location_query)
    if title_query:
        profiles = profiles.filter(title__icontains=title_query)
    if region_query:
        profiles = profiles.filter(region__iexact=region_query)
    regions = PostProfile.REGIONS_CHOICES

    context = {
        'profiles': profiles,
        'location_query': location_query,
        'title_query': title_query,
        'region_query': region_query,
        'regions': regions,
    }
    return render(request, 'profile_list.html', context)


def posts_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    posts = PostProfile.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'posts_by_category.html', context)



from .models import Report, PostProfile 
from django.shortcuts import render, get_object_or_404, redirect
from app.models import PostProfile
from django.contrib.auth.decorators import login_required
from .forms import  ReportProfileForm
from .forms import CommentForm
from .models import Comment
import geocoder
import folium

def job_details(request, post_id):
    post = get_object_or_404(PostProfile, pk=post_id)
    report_form = ReportProfileForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)
    job_location = geocoder.osm(post.location)
    if job_location.lat is not None and job_location.lng is not None:
        job_map = folium.Map(location=[job_location.lat, job_location.lng], zoom_start=10)
        folium.Marker([job_location.lat, job_location.lng], popup=post.title).add_to(job_map)
        job_map = job_map._repr_html_()
    else:
        job_map = None

    if request.method == 'POST':
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.user = request.user
            report.post_profile = post
            report.save()
            return redirect('job_details', post_id=post_id)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post_profile = post
            comment.save()
            return redirect('job_details', post_id=post_id)

    comments = Comment.objects.filter(post_profile=post)

    context = {
        'post': post,
        'job_map': job_map,
        'report_form': report_form,
        'comment': comment_form, 
        'comments': comments,
    }
    return render(request, 'job_details.html', context)










from .models import Vacancy
from django.db.models import Q
from .models import Vacancy
from .forms import VacancySearchForm
from django.utils import timezone

def all_vacancies(request):
    form = VacancySearchForm(request.GET)
    vacancies = Vacancy.objects.filter(is_approved=True, deadline__gte=timezone.now())
    if form.is_valid():
        title = form.cleaned_data['title']
        location = form.cleaned_data['location']
        region_query = request.GET.get('region')
        if title:
            vacancies = vacancies.filter(title__icontains=title)
        if location:
            vacancies = vacancies.filter(location__icontains=location)
        if region_query:
             vacancies = vacancies.filter(regions__iexact=region_query)
        regions = Vacancy.REGIONS_CHOICES

    context = {
        'featured_vacancies': vacancies,
        'search_form': form,
'region_query': region_query,
        'regions': regions,
    }
    return render(request, 'all_vacancies.html', context)








from django.contrib.auth.decorators import login_required, user_passes_test
from .models import VacancyApplication

def is_vacancy_owner(user, vacancy):
    return user == vacancy.user

@login_required
@user_passes_test(lambda u: u.is_superuser or is_vacancy_owner(u, vacancy), login_url='/login/')
def applicant_list(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    applications = VacancyApplication.objects.filter(vacancy=vacancy)
    
    return render(request, 'applicant_list.html', {'vacancy': vacancy, 'applications': applications})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vacancy, VacancyApplication

@login_required
def vacancy_applicants(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.user != vacancy.user:
        return redirect('index') 
    applicants = VacancyApplication.objects.filter(vacancy=vacancy)
    return render(request, 'applicant_details.html', {'applicants': applicants, 'post': vacancy})



from .models import Vacancy
from .forms import VacancyApplicationForm
def vacancyDetails(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    job_location = geocoder.osm(vacancy.location)
    if job_location.lat is not None and job_location.lng is not None:
        job_map = folium.Map(location=[job_location.lat, job_location.lng], zoom_start=10)
        folium.Marker([job_location.lat, job_location.lng], popup=vacancy.title).add_to(job_map)
        job_map = job_map._repr_html_()
    else:
        job_map = None
    if request.method == 'POST':
        form = VacancyApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = vacancy
            application.save()
            return redirect('details', pk=pk)
    else:
        form = VacancyApplicationForm()
    return render(request, 'all_vacancy_details.html', {'post': vacancy, 'form': form,'job_map': job_map, })


from .forms import CreateVacancyForm
def create_vacancy(request):
    if request.method == 'POST':
        form = CreateVacancyForm(request.POST, request.FILES)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.user = request.user
            vacancy.save()
            return redirect('index')  # Replace 'vacancy_list' with your actual URL name
    else:
        form = CreateVacancyForm()

    context = {
        'form': form,
    }
    return render(request, 'create_vacancy.html', context)



def posts_by_region(request, region_name):
    posts = PostProfile.objects.filter(region=region_name)
    context = {
        'posts': posts,
        'region_name': region_name,
    }
    return render(request, 'posts_by_region.html', context)



def manage_profiles(request):
    show_approved = request.GET.get('show_approved')
    if show_approved:
        profiles = PostProfile.objects.filter(is_approved=True)
    else:
        profiles = PostProfile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'manage_profiles.html', context)



from django.shortcuts import redirect
def approve_profile(request, profile_id):
    profile = PostProfile.objects.get(pk=profile_id)
    if request.method == 'POST':
        if 'approved' in request.POST:
            profile.is_approved = True
        else:
            profile.is_approved = False
        profile.save()
    return redirect('manage_profiles')



def update_profile(request, profile_id):
    profile = get_object_or_404(PostProfile, id=profile_id)
    if request.method == 'POST':
        form = PostProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('manage_profiles')
    else:
        form = PostProfileForm(instance=profile)
    context = {'form': form}
    return render(request, 'update_profile.html', context)

def delete_profile(request, profile_id):
    profile = get_object_or_404(PostProfile, pk=profile_id)
    if request.method == 'POST':
        profile.delete()
        return redirect('manage_profiles')
    context = {'profile': profile}
    return render(request, 'delete_profile.html', context)


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages


def user_login(request):
    form = AuthenticationForm()  # Define form here to ensure it's available in all paths
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password. Please check your credentials.')
    return render(request, 'login.html', {'form': form})



from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user_login')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('index')


def about(request):
    logout(request)
    return render(request, 'about.html')






