from django.forms import ModelForm
from django import forms
from .models import contact, PostProfile, Category, Report, Comment



class ReportProfileForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['email', 'phone_number', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control white-bg-textarea'}),
        }



class contactform(ModelForm):
    class Meta:
        model = contact
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'availability_type': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'charges': forms.NumberInput(attrs={'class': 'form-control'}),
            'sample_works': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'skills_abilities': forms.Textarea(attrs={'class': 'form-control'}),
            
        }
 
        

class PostProfileForm(forms.ModelForm):
    class Meta:
        model = PostProfile
        exclude = ['date_posted', 'is_approved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'availability_type': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'charges': forms.NumberInput(attrs={'class': 'form-control'}),
            'sample_works': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'skills_abilities': forms.Textarea(attrs={'class': 'form-control'}),
            
        }
 
        
from .models import VacancyApplication

class VacancyApplicationForm(forms.ModelForm):
    class Meta:
        model = VacancyApplication
        fields = ['name', 'email', 'telephone',  'message' , 'cv']        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cv': forms.FileInput(attrs={'class': 'form-control-file'}),
            
        }
        
from django import forms
from .models import Vacancy
class VacancySearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
 
from .models import Vacancy
class CreateVacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['user', 'date_posted', 'is_approved']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'telephone': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'rows': 4}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}, choices=Vacancy.CATEGORY_CHOICES),
            'regions': forms.Select(attrs={'class': 'form-control'}, choices=Vacancy.REGIONS_CHOICES),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_too_short': _("Your password must contain at least 8 characters."),
        'password_common': _("Your password can't be a commonly used password."),
        'password_entirely_numeric': _("Your password can't be entirely numeric."),
    }
    
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("Your custom password requirements here."),  # Customize this
        error_messages={
            'required': _("Password is required."),
            'password_mismatch': _("The two passwords didn't match."),
            'password_too_short': _("Your password must contain at least 8 characters."),
            'password_common': _("Your password can't be a commonly used password."),
            'password_entirely_numeric': _("Your password can't be entirely numeric."),
        },
    )
    
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

from .models import Comment





















