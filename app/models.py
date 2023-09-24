from django.db import models

# Create your models here.


class contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name  + '|| ' + self.email 
    



from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



from django.utils import timezone
class PostProfile(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    REGIONS_CHOICES = [
    ('ashanti', 'Ashanti Region'),
    ('brong', 'Brong Region'),
    ('central', 'Central Region '),
    ('eastern', 'Eastern Region '),
    ('greater_accra', 'Greater Accra Region'),
    ('northern', 'Northern Region '),
    ('savannah', 'Savannah Region '),
    ('north_east', 'North-East Region '),
    ('upper_east', 'Upper East Region '),
    ('bono_east', 'Bono East Region '),
    ('ahafo', 'Ahafo Region '),
    ('oti', 'Oti Region '),
    ('volta', 'Volta Region'),
    ('western', 'Western Region'),
    ('western_north', 'Western North Region'),
    ('upper_west', 'Upper West Region '),
]

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        
    ]
    EDU_LEVEL = [
        ('JHS', 'JHS'),
        ('SHS', 'SHS'),
        ('Tertiary', 'Tertiary'),
        ('None', 'None'),
        ('Other', 'Other'),
        
    ]
    AVAILABILITY_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ]
    availability_type = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)
    age = models.IntegerField()
    sex = models.CharField(max_length=20, choices=GENDER)
    region = models.CharField(max_length=20, choices=REGIONS_CHOICES)
    charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    education_level = models.CharField(max_length=20, choices=EDU_LEVEL)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    sample_works = models.ImageField(upload_to='sample_works/', null=True, blank=True)
    description = models.TextField()
    skills_abilities = models.TextField()
    date_posted = models.DateField(auto_created=True,default=timezone.now)
    is_approved = models.BooleanField(default=False)
        
    def __str__(self):
        return self.title



from django.contrib.auth.models import User

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_profile = models.ForeignKey(PostProfile, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.IntegerField()
    message = models.TextField()
    submission_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report by {self.post_profile}"

    

from django.db import models



class Vacancy(models.Model):
    REGIONS_CHOICES = [
    ('ashanti', 'Ashanti Region'),
    ('brong', 'Brong Region'),
    ('central', 'Central Region '),
    ('eastern', 'Eastern Region '),
    ('greater_accra', 'Greater Accra Region'),
    ('northern', 'Northern Region '),
    ('savannah', 'Savannah Region '),
    ('north_east', 'North-East Region '),
    ('upper_east', 'Upper East Region '),
    ('bono_east', 'Bono East Region '),
    ('ahafo', 'Ahafo Region '),
    ('oti', 'Oti Region '),
    ('volta', 'Volta Region'),
    ('western', 'Western Region'),
    ('western_north', 'Western North Region'),
    ('upper_west', 'Upper West Region '),
]
    CATEGORY_CHOICES = [
        ('Information Technology', 'Information Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Marketing and Advertising', 'Marketing and Advertising'),
        ('Education', 'Education'),
        ('Engineering', 'Engineering'),
        ('Sales', 'Sales'),
        ('Human Resources', 'Human Resources'),
        ('Art and Design', 'Art and Design'),
        ('Science', 'Science'),
        ('Construction and Trades', 'Construction and Trades'),
        ('Legal', 'Legal'),
        ('Customer Service', 'Customer Service'),
        ('Media and Journalism', 'Media and Journalism'),
        ('Transportation and Logistics', 'Transportation and Logistics'),
        ('Other', 'Other'),
    ]
    company_name= models.CharField(max_length=20, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=20, blank=True, null=True)
    telephone = models.IntegerField()
    email = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    categories = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    regions = models.CharField(max_length=50, choices=REGIONS_CHOICES)
    skills = models.CharField(max_length=200)
    salary = models.CharField(max_length=50, blank=True, null=True)
    deadline = models.DateField()
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    date_posted = models.DateField(auto_created=True,default=timezone.now)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class VacancyApplication(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telephone = models.IntegerField(null=False, blank=True)
    message = models.TextField(blank=True)
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    date_posted = models.DateField(auto_created=True,default=timezone.now)

    
    def __str__(self):
        return f"Application for {self.vacancy.title} by {self.name}"


from django.utils import timezone

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_profile = models.ForeignKey(PostProfile, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.user.username} - {self.post_profile.title} - {self.date.date}"



















