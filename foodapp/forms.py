from django import forms
from .models import FoodMakerProfile, EaterProfile

from django.contrib.auth.forms import UserCreationForm
from .models import User

from django import forms
from .models import FoodItem

from django import forms
from .models import FoodMakerProfile


class FoodMakerProfileForm(forms.ModelForm):
    class Meta:
        model = FoodMakerProfile
        fields = ['first_name', 'last_name', 'street_name', 'city', 'state', 'zipcode', 'bio', 'business_name', 'address', 'phone_number']


class EaterProfileForm(forms.ModelForm):
    preferences = forms.CharField(required=False)  # Make preferences optional
    class Meta:
        model = EaterProfile
        fields = ['phone_number', 'preferences']  # Fixed field order


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Exclude 'role' as it's set manually


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['title', 'description', 'ingredients', 'price', 'cuisine', 'food_type', 'food_protien', 'food_image', 'food_image2', 'food_image3']


class FoodMakerProfileForm(forms.ModelForm):
    preparation_time = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'step': '0.5',  # Increment by 0.5
            'min': '0.5',   # Minimum value
            'max': '24',    # Maximum value (24 hours)
        }),
        label="Preparation Time (hours)"
    )

    class Meta:
        model = FoodMakerProfile
        fields = [
            'first_name', 'last_name', 'street_name', 'city', 'zipcode', 'bio', 
            'website_url', 'specialized_cuisines', 'preparation_time', 
            'business_name', 'address', 'phone_number', 'state', 'address'
        ]


class ContactForm(forms.Form):
    WHO_CHOICES = [
        ('subscriber', 'Subscriber'),
        ('want_to_join', 'Want to Join'),
    ]

    ISSUE_CHOICES = [
        ('general', 'General Questions'),
        ('website_issue', 'Website Issue'),
        ('login_issue', 'Account Login Issue'),
        ('billing_issue', 'Account Billing Issue'),
        ('other', 'Other'),
    ]

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    who_are_you = forms.ChoiceField(choices=WHO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    issue_type = forms.ChoiceField(choices=ISSUE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
