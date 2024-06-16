from django.contrib import admin
from .models import *

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'license_plate', 'color', 'price_per_day', 'category', 'is_available')
    list_filter = ('make', 'color', 'category', 'is_available')
    search_fields = ('make', 'model', 'license_plate')
    fieldsets = (
        (None, {
            'fields': ('make', 'model', 'year', 'license_plate', 'color', 'image', 'price_per_day', 'category', 'is_available')
        }),
    )

@admin.register(VehicleReservation)
class VehicleReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle','user', 'start_time', 'end_time')
    search_fields = ('vehicle__make', 'vehicle__model', 'start_time', 'end_time')


admin.site.register(Korisnik)
