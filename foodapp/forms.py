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

