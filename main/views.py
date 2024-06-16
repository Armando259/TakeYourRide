from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, TemplateView, UpdateView, CreateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta
import json
from .models import *
from .form import *


def about(request):
    return render(request, 'about.html')

@login_required
def profile_view(request):
    korisnik, created = Korisnik.objects.get_or_create(user=request.user, defaults={
        'ime_korisnika': '',
        'prezime_korisnika': '',
        'adresa_korisnika': '',
        'mobitel_korisnika': '',
        'email_korisnika': request.user.email
    })
    return render(request, 'profile.html', {'korisnik': korisnik})

@login_required
def update_profile(request):
    korisnik = get_object_or_404(Korisnik, user=request.user)
    if request.method == 'POST':
        form = korisnikForm(request.POST, instance=korisnik)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil je uspješno ažuriran.')
            return redirect('main:profile')
        else:
            messages.error(request, 'Molimo ispravite greške ispod.')
    else:
        form = korisnikForm(instance=korisnik)
    
    return render(request, 'update_profile.html', {'form': form})

class LandingPageView(ListView):
    model = Vehicle
    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        kate = Vehicle.objects.all() 
        return render(request, 'landing.html', {'kate': kate})

def login_user (request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            messages.success(request, ("Krivi unos! Pokusajte ponovo..."))	
            return redirect('main:login')
    else:
        return render(request, 'registration/login.html', {})
def logout_user (request):
    logout(request)
    return redirect('main:home') 


def register(request):
    if request.method == 'POST':
        form1 = korisnikForm(request.POST)
        form = RegisterUserForm(request.POST)

        if form.is_valid() and form1.is_valid():
            user = form.save(commit=False)
            user.save()
            korisnik = form1.save(commit=False)
            korisnik.user = user
            korisnik.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main:home')

    else:
        form1 = korisnikForm()
        form = RegisterUserForm()

    context = {'form': form, 'form1': form1}

    return render(request, 'registration/register.html', context)



def home(request):
    return render(request, 'home.html')


def vehicle_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search_query', '')

    vehicles = Vehicle.objects.all()

    if category:
        vehicles = vehicles.filter(category=category)

    if search_query:
        vehicles = vehicles.filter(
            models.Q(make__icontains=search_query) |
            models.Q(model__icontains=search_query) |
            models.Q(license_plate__icontains=search_query)
        )

    categories = Vehicle.CATEGORY_CHOICES
    return render(request, 'vehicles.html', {'vehicles': vehicles, 'categories': categories, 'search_query': search_query})


class DeleteVehicleView(DeleteView):
    model = Vehicle
    template_name = 'vehicle_confirm_delete.html'
    success_url = reverse_lazy('main:vehicles') 

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.none()
        return super().get_queryset()

@login_required
def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if not vehicle.is_available:
        messages.error(request, "Vozilo trenutno nije dostupno za iznajmljivanje.")
        return redirect('main:vehicles')

    if request.method == 'POST':
        form = RentalForm(request.POST, initial_vehicle=vehicle)
        if form.is_valid():
            new_reservation = form.save(commit=False)
            new_reservation.user = request.user  
            new_reservation.vehicle = vehicle  
            overlapping_reservations = VehicleReservation.objects.filter(
                vehicle=vehicle,
                start_time__lt=new_reservation.end_time,
                end_time__gt=new_reservation.start_time
            ) | VehicleReservation.objects.filter(
                vehicle=vehicle,
                end_time=new_reservation.start_time
            ) | VehicleReservation.objects.filter(
                vehicle=vehicle,
                start_time=new_reservation.end_time
            )
            if overlapping_reservations.exists():
                messages.error(request, "Auto je već rezerviran za odabrani period.")
            else:
                new_reservation.save()
                messages.success(request, "Vaša rezervacija je uspješno kreirana.")
                return redirect('main:vehicle_detail', vehicle_id=vehicle.pk)
        else:
            print(form.errors)  
    else:
        form = RentalForm(initial_vehicle=vehicle)

    return render(request, 'vehicle_detail.html', {'vehicle': vehicle, 'form': form})



def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:vehicles')
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('main:vehicles')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'edit_vehicle.html', {'form': form, 'vehicle': vehicle})




@require_GET
def reservation_events(request, vehicle_id):
    reservations = VehicleReservation.objects.filter(vehicle_id=vehicle_id)
    events = []
    for reservation in reservations:
        events.append({
            'title': '',
            'start': reservation.start_time.date().isoformat(),  
            'end': (reservation.end_time.date() + timedelta(days=1)).isoformat(),  
            'allDay': True,  
            'user': reservation.user.username,  

        })
    return JsonResponse(events, safe=False)