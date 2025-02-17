from django import forms
from .models import FoodMakerProfile, EaterProfile


from django.contrib.auth.forms import UserCreationForm
from .models import User

from django import forms
from .models import FoodItem


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
