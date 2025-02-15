from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User Model that includes a 'role' field
class User(AbstractUser):
    ROLE_CHOICES = [
        ('Eater', 'Eater'),
        ('FoodMaker', 'FoodMaker'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Avoid reverse accessor conflicts with Group and Permission
    groups = models.ManyToManyField(
        Group,
        related_name='foodapp_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='foodapp_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# FoodMaker Profile Model
class FoodMakerProfile(models.Model):
    US_STATES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="foodmaker_profile")  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    bio = models.TextField(blank=True)
    business_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    state = models.CharField(max_length=2, choices=US_STATES)
    is_subscribed = models.BooleanField(default=False)  # Subscription status
    subscription_expiry = models.DateField(null=True, blank=True)  # Expiry date

    def __str__(self):
        return self.user.username


# Eater Profile Model
class EaterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="eater_profile")  
    phone_number = models.CharField(max_length=15)
    preferences = models.TextField(blank=True)  

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Food Item Model (for FoodMakers to add food items)
class FoodItem(models.Model):
    foodmaker = models.ForeignKey(FoodMakerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cuisine = models.CharField(max_length=100)

    food_type = models.CharField(max_length=100, default='Snacks')
    food_protien = models.CharField(max_length=100, default="None")

    food_image = models.ImageField(upload_to='food_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    


class PromoCode(models.Model):
    
    code = models.CharField(max_length=20, unique=True)  # Promo code (e.g., SAVE10)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # Discount amount (flat or percentage)
    is_percentage = models.BooleanField(default=True)  # If True, it's a percentage discount
    valid_from = models.DateTimeField()  # Start date of promo
    valid_to = models.DateTimeField()  # End date of promo
    is_active = models.BooleanField(default=True)  # Toggle promo availability


    def __str__(self):
        return f"{self.code} - ${self.discount} off"


'''
# Order Model (To handle food orders by Eaters)
class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    eater = models.ForeignKey(EaterProfile, related_name='orders', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, related_name='orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def save(self, *args, **kwargs):
        # Automatically calculate total price based on quantity and food item price
        self.total_price = self.quantity * self.food_item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.eater.user.username} -  {self.status}"
'''