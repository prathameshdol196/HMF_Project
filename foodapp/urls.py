from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),  # Food Detail Page
    path('foodmaker/<int:foodmaker_id>/', views.foodmaker_profile, name='foodmaker_profile'),


    path('register/', views.register, name='register'),  # Main registration page
    path('register/foodmaker/', views.register_foodmaker, name='register_foodmaker'),
    path('register/eater/', views.register_eater, name='register_eater'),

    path('dashboard/foodmaker/', views.foodmaker_dashboard, name='foodmaker_dashboard'),
    path('dashboard/eater/', views.eater_dashboard, name='eater_dashboard'),

    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('dashboard/foodmaker/', views.foodmaker_dashboard, name='foodmaker_dashboard'),
    path('dashboard/eater/', views.eater_dashboard, name='eater_dashboard'),

    path('add-food/', views.add_food, name='add_food'),
    path('update-food/<int:food_id>/', views.update_food, name='update_food'),
    path('delete-food/<int:food_id>/', views.delete_food, name='delete_food'),

    #path("order/<int:food_id>/", views.place_order, name="place_order"),
    #path("eater/orders/", views.eater_orders, name="eater_orders"),
    #path("foodmaker/orders/", views.foodmaker_orders, name="foodmaker_orders"),
    #path("order/update/<int:order_id>/", views.update_order_status, name="update_order_status"),
    #path('order/<int:order_id>/status/', views.update_order_status, name='update_order_status'),

]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)