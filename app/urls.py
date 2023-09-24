from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
path('', views.index, name='index'),
path('contact', views.contact, name='contact')  ,  
path('create_post_profile', views.create_post_profile, name='create_post_profile')    ,
path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
path('categories/', views.all_categories, name='all_categories'),
path('profile_list', views.profile_list, name="profile_list"),
path('job/<int:post_id>/', views.job_details, name='job_details'),
path('region/<str:region_name>/', views.posts_by_region, name='posts_by_region'),
path('manage_profiles/', views.manage_profiles, name='manage_profiles'),
path('update_profile/<int:profile_id>/', views.update_profile, name='update_profile'),
path('delete_profile/<int:profile_id>/', views.delete_profile, name='delete_profile'),
path('user_login', views.user_login, name='user_login')  ,  
path('user_signup', views.user_signup, name='user_signup')  ,  
path('logout/', views.logout_view, name='logout'),
path('about', views.about, name='about')  ,  
path('add_category/', views.add_category, name='add_category'),
path('approve_profile/<int:profile_id>/',views. approve_profile, name='approve_profile'),
path('create_vacancy/', views.create_vacancy, name='create_vacancy'),
path('all_vacancies/', views.all_vacancies, name='all_vacancies'),
path('vacancy/<int:pk>/', views.vacancyDetails, name='details'),
path('applicants/<int:vacancy_id>/', views.applicant_list, name='applicant_list'),
path('vacancy_applicants/<int:pk>/', views.vacancy_applicants, name='vacancy_applicants'),
path('search', views.search_results, name='search_results'),
 
 
 

    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)








