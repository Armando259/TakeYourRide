from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms

class Vehicle(models.Model):
    MAKE_CHOICES = [
    ('toyota', 'Toyota'),
    ('ford', 'Ford'),
    ('bmw', 'BMW'),
    ('audi', 'Audi'),
    ('mercedes', 'Mercedes-Benz'),
    ('honda', 'Honda'),
    ('chevrolet', 'Chevrolet'),
    ('nissan', 'Nissan'),
    ('volkswagen', 'Volkswagen'),
    ('hyundai', 'Hyundai'),
    ]

    COLOR_CHOICES = [
    ('crvena', 'Crvena'),
    ('plava', 'Plava'),
    ('zelena', 'Zelena'),
    ('crna', 'Crna'),
    ('bijela', 'Bijela'),
    ('srebrna', 'Srebrna'),
    ('žuta', 'Žuta'),
    ('narančasta', 'Narančasta'),
    ('ljubičasta', 'Ljubičasta'),
    ('smeđa', 'Smeđa'),
]

    
    CATEGORY_CHOICES = [
        ('mali', 'Mali'),
        ('srednji', 'Srednji'),
        ('veliki', 'Veliki'),
        ('kombi', 'Kombi'),
    ]

    make = models.CharField(max_length=20, choices=MAKE_CHOICES)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=10)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='mali')

    def __str__(self):
        return f"{self.get_make_display()} {self.model}"
    

class VehicleReservation(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.vehicle} reserved by {self.user} from {self.start_time} to {self.end_time}"
    
class Korisnik(models.Model):
    ime_korisnika = models.CharField(max_length=100)
    prezime_korisnika = models.CharField(max_length=100)
    adresa_korisnika = models.CharField(max_length=100)
    mobitel_korisnika = models.CharField(max_length=10)
    email_korisnika = models.EmailField()
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.email_korisnika
    


