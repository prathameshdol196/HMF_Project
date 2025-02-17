from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, authenticate
from .forms import FoodMakerProfileForm, EaterProfileForm, CustomUserCreationForm
from .models import FoodMakerProfile, EaterProfile  # Ensure correct imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import PromoCode
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Q

from .models import User


User = get_user_model()


'''# Home Page
def home(request):
    
    food_items = FoodItem.objects.all()  # Fetch all food items

    # Get filter values from request
    cuisine = request.GET.get('cuisine')
    city = request.GET.get('city')
    zipcode = request.GET.get('zipcode')
    foodmaker = request.GET.get('foodmaker')
    state = request.GET.get('state')


    # Apply filters if selected
    if cuisine:
        food_items = food_items.filter(cuisine__icontains=cuisine)
    if city:
        food_items = food_items.filter(foodmaker__city__icontains=city)
    if zipcode:
        food_items = food_items.filter(foodmaker__zipcode=zipcode)
    if foodmaker:
        food_items = food_items.filter(foodmaker_id=foodmaker)
    if state:
        food_items = food_items.filter(foodmaker__state=state)

    # Get distinct values for filters
    cuisines = FoodItem.objects.values_list('cuisine', flat=True).distinct()
    cities = FoodItem.objects.values_list('foodmaker__city', flat=True).distinct()
    zipcode = FoodItem.objects.values_list('foodmaker__zipcode', flat=True).distinct()
    state = FoodItem.objects.values_list('foodmaker__state', flat=True).distinct()
    foodmakers = FoodMakerProfile.objects.all()


    return render(request, 'home.html', {
        'food_items': food_items,
        'cuisines': cuisines,
        'cities': cities,
        'zipcodes': zipcode,
        'state': state,
        'foodmakers': foodmakers,
    })

'''

# Home Page
def home(request):
    food_items = FoodItem.objects.all()  # Fetch all food items

    # Get distinct cuisines from available food items
    cuisines = FoodItem.objects.values_list('cuisine', flat=True).distinct()

    # Get filter values from request
    query = request.GET.get('q', '')  # Get search query
    cities = [request.GET.get(f'city{i}', '') for i in range(1, 4)]  # Get up to 3 selected cities
    selected_cuisines = request.GET.getlist('cuisine')
    state = request.GET.get('state')

    # Apply search filter
    if query:
        food_items = food_items.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Apply multiple city filters
    selected_cities = [city for city in cities if city]  # Remove empty values
    if selected_cities:
        food_items = food_items.filter(foodmaker__city__in=selected_cities)

    # Apply cuisine filter
    if selected_cuisines:
        food_items = food_items.filter(cuisine__in=selected_cuisines)

    # Apply state filter
    if state:
        food_items = food_items.filter(foodmaker__state=state)

    # Get distinct values for dropdowns
    all_cities = FoodItem.objects.values_list('foodmaker__city', flat=True).distinct()
    states = FoodItem.objects.values_list('foodmaker__state', flat=True).distinct()
    
    return render(request, 'home.html', {
        'food_items': food_items,
        'cuisines': cuisines,
        'cities': all_cities,
        'states': states,
        'selected_cuisines': selected_cuisines,
        'query': query,
        'selected_cities': selected_cities,
    })

def select_food(request):
    # Get search query, selected cuisines, and selected cities
    query = request.GET.get('q', '')
    selected_cuisines = request.GET.getlist('cuisine')
    cities = [request.GET.get(f'city{i}', '') for i in range(1, 4)]
    selected_cities = [city for city in cities if city]

    # Start with all food items and filter based on user inputs
    # foodmakers = FoodMakerProfile.objects.prefetch_related('food_items').all()
    
    # Start with all food items
    food_items = FoodItem.objects.select_related('foodmaker').all()

    # Filter by search query
    if query:
        food_items = food_items.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Filter by selected cuisines
    if selected_cuisines:
        food_items = food_items.filter(cuisine__in=selected_cuisines)

    # Filter by selected cities
    if selected_cities:
        food_items = food_items.filter(foodmaker__city__in=selected_cities)

    # Get only the FoodMakers that have matching food items
    foodmakers = FoodMakerProfile.objects.filter(id__in=food_items.values_list('foodmaker_id', flat=True)).prefetch_related("food_items")
    

    # Pass results to the template
    return render(request, 'select_food.html', {
        'food_items': food_items,
        'selected_cuisines': selected_cuisines,
        'query': query,
        'foodmakers': foodmakers,
        'selected_cities': selected_cities,
    })



def about(request):
    return render(request, 'about.html')


def food_detail(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)  # Fetch food by ID
    foodmaker = food_item.foodmaker  # Get associated FoodMakerProfile

    discounted_price = food_item.price  # Default to original price
    promo_code_message = ""  # Message for promo code result

    if request.method == "POST":
        promo_code_input = request.POST.get("promo_code", "").strip()  # Get user input
        try:
            promo = PromoCode.objects.get(code=promo_code_input, is_active=True)

            if promo.valid_from <= now() <= promo.valid_to:  # Check if promo is active
                if promo.is_percentage:
                    discount_amount = (food_item.price * promo.discount) / 100
                else:
                    discount_amount = promo.discount

                discounted_price = max(food_item.price - discount_amount, 0)  # Ensure non-negative price
                promo_code_message = f"Promo code applied! You saved ${discount_amount:.2f}!"
            else:
                promo_code_message = "This promo code has expired."

        except PromoCode.DoesNotExist:
            promo_code_message = "Invalid promo code."

    return render(request, 'food_detail.html', {
        'food_item': food_item, 
        'foodmaker': foodmaker,
        'discounted_price': discounted_price,
        'promo_code_message': promo_code_message
        
        })


def foodmaker_profile(request, foodmaker_id):
    foodmaker = get_object_or_404(FoodMakerProfile, id=foodmaker_id)
 
    food_items = FoodItem.objects.filter(foodmaker=foodmaker)  # Get their food items
    return render(request, 'foodmaker_profile.html', {
        'foodmaker': foodmaker, 
        'food_items': food_items
        })


# Main Register Page
def register(request):
    return render(request, 'register.html')


# Register as FoodMaker
def register_foodmaker(request):
    print("inside register foodmaker")

    if request.method == 'POST':
        print("inside if")

        form = CustomUserCreationForm(request.POST)  # Use Custom Form
        foodmaker_form = FoodMakerProfileForm(request.POST)

        username = request.POST.get("username")
        email = request.POST.get("email")

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please log in instead.")
            return redirect("login")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered as a FoodMaker. Please log in instead.")
            return redirect("login")


        if form.is_valid() and foodmaker_form.is_valid():
            print("inside second if")
            
            # Save the user instance
            user = form.save(commit=False)  
            user.role = 'FoodMaker'  # Assign role
            user.save()  # Now save the user
            
            # Save the foodmaker profile
            foodmaker_profile = foodmaker_form.save(commit=False)
            foodmaker_profile.user = user  # Assign the user instance
            foodmaker_profile.save()

            login(request, user)  # Log in the user
            print("User registered and logged in:", user)
            
            return redirect('foodmaker_dashboard')  # Redirect after successful registration

        else:
            print("Form Errors:")
            print("UserCreationForm Errors:", form.errors)
            print("FoodMakerProfileForm Errors:", foodmaker_form.errors)

    else:
        print("inside else")
        form = CustomUserCreationForm()
        foodmaker_form = FoodMakerProfileForm()
    
    return render(request, 'register_foodmaker.html', {
        'form': form, 
        'foodmaker_form': foodmaker_form
        })


# Register as Eater
def register_eater(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use Custom Form
        eater_form = EaterProfileForm(request.POST)

        username = request.POST.get("username")
        email = request.POST.get("email")

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please log in instead.")
            return redirect("login")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered as a Eater. Please log in instead.")
            return redirect("login")


        
        if form.is_valid() and eater_form.is_valid():
            user = form.save(commit=False)
            user.role = 'Eater'  # Set the role to Eater
            user.save()

            eater_profile = eater_form.save(commit=False)
            eater_profile.user = user  # Link to the user
            eater_profile.save()

            login(request, user)  # Log the user in after registration
            return redirect('eater_dashboard')  # Redirect to Eater dashboard

    else:
        form = CustomUserCreationForm()
        eater_form = EaterProfileForm()

    return render(request, 'register_eater.html', {
        'form': form, 
        'eater_form': eater_form
        })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in

                # Redirect based on role
                if user.role == 'FoodMaker':
                    return redirect('foodmaker_dashboard')  # Redirect to FoodMaker Dashboard
                elif user.role == 'Eater':
                    return redirect('eater_dashboard')  # Redirect to Eater Dashboard

        else:
            print("Login failed. Errors:", form.errors)

    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# Eater Dashboard
@login_required
def eater_dashboard(request):
    if request.user.role != 'Eater':
        return redirect('home')  # Redirect to home or show an error page if the user is not an eater
    
    eater_profile = EaterProfile.objects.get(user=request.user)
        
    # Fetch all orders for this EaterProfile
    #orders = Order.objects.filter(eater=eater_profile)
    
    return render(request, 'eater_dashboard.html')


# FoodMaker Dashboard
@login_required
def foodmaker_dashboard(request):
    if request.user.role != 'FoodMaker':
        return redirect('home')  # Redirect to home or show an error page if the user is not a foodmaker
    
    food_items = FoodItem.objects.filter(foodmaker=request.user.foodmaker_profile)
    return render(request, 'foodmaker_dashboard.html', {'food_items': food_items})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodItem, FoodMakerProfile
from .forms import FoodForm


@login_required
def add_food(request):
    if request.user.role != 'FoodMaker':
        return redirect('home')

    if not hasattr(request.user, 'foodmaker_profile'):
        return redirect('home')  # Redirect non-FoodMakers

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.foodmaker = request.user.foodmaker_profile  # FIXED ATTRIBUTE
            food.save()
            return redirect('foodmaker_dashboard')  # Redirect after adding
    else:
        form = FoodForm()

    return render(request, 'add_food.html', {'form': form})


@login_required
def update_food(request, food_id):
    if request.user.role != 'FoodMaker':
        return redirect('home')

    food = get_object_or_404(FoodItem, id=food_id)

    # Ensure only the owner can update
    if food.foodmaker != request.user.foodmaker_profile:
        return redirect('home')  # Unauthorized access

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('foodmaker_dashboard')  # Redirect after update
    else:
        form = FoodForm(instance=food)

    return render(request, 'update_food.html', {
        'form': form, 
        'food': food
        })


@login_required
def delete_food(request, food_id):
    if request.user.role != 'FoodMaker':
        return redirect('home')

    food = get_object_or_404(FoodItem, id=food_id)

    # Ensure only the owner can delete
    if food.foodmaker != request.user.foodmaker_profile:
        return redirect('home')  # Unauthorized access

    if request.method == 'POST':
        food.delete()
        return redirect('foodmaker_dashboard')  # Redirect after deletion

    return render(request, 'delete_food.html', {'food': food})



'''from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from .models import FoodItem, Order, EaterProfile, FoodMakerProfile
import json

# View to place an order
@login_required
def place_order(request, food_id):
    if request.method == "POST":
        try:
            eater_profile = EaterProfile.objects.get(user=request.user)
            food_item = get_object_or_404(FoodItem, id=food_id)
            foodmaker = food_item.foodmaker  # Get the FoodMakerProfile

            quantity = request.POST.get("quantity", 1)  # Default quantity is 1

            # Ensure quantity is an integer
            quantity = int(quantity)

            # Calculate total price
            total_price = food_item.price * Decimal(quantity)

            # Create the order
            Order.objects.create(
                eater=eater_profile,
                food_item=food_item,
                quantity=quantity,
                total_price=total_price,
            )

            # Add a success message
            messages.success(request, "Order placed successfully!")

            # Redirect to home page
            return redirect('home')

        except EaterProfile.DoesNotExist:
            messages.error(request, "Eater profile not found.")
            return redirect('home')

    # If it's not a POST request, return an error
    messages.error(request, "Invalid request.")
    return redirect('home')


# View for foodmakers to see orders placed for their food
@login_required
def foodmaker_orders(request):

    if not request.user.role == "FoodMaker":
        return redirect('home')
    
    foodmaker_profile = get_object_or_404(FoodMakerProfile, user=request.user)
    orders = Order.objects.filter(foodmaker=foodmaker_profile).order_by('-order_date')
    return render(request, "foodmaker_orders.html", {"orders": orders})

'''




