from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from .views import *
from django.contrib import admin
app_name = 'main'  


urlpatterns = [

    path('about/', views.about, name='about'),  
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('', views.LandingPageView.as_view(), name='landing'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('vehicles/', views.vehicle_list, name='vehicles'),  
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
    path('home/', home, name='home'),
    path('api/reservations/<int:vehicle_id>/', views.reservation_events, name='reservation_events'),
    path('vehicles/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicle/<int:pk>/delete/', views.DeleteVehicleView.as_view(), name='delete_vehicle'),

]

   
 
