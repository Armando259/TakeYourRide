from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tempus_dominus.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone



class korisnikForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ['ime_korisnika', 'prezime_korisnika', 'adresa_korisnika', 'mobitel_korisnika', 'email_korisnika']
        labels = {
            'ime_korisnika': 'Ime',
            'prezime_korisnika': 'Prezime',
            'adresa_korisnika': 'Adresa',
            'mobitel_korisnika': 'Mobitel',
            'email_korisnika': 'Email',
        }
        widgets = {
            'ime_korisnika': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ime'}),
            'prezime_korisnika': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prezime'}),
            'adresa_korisnika': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresa'}),
            'mobitel_korisnika': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobitel'}),
            'email_korisnika': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }



class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'license_plate', 'color', 'image', 'is_available', 'price_per_day', 'category']
        widgets = {
            'make': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Spremi'))
        
         
class RegisterUserForm(UserCreationForm):	

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'





class RentalForm(forms.ModelForm):
    class Meta:
        model = VehicleReservation
        fields = ['vehicle', 'start_time', 'end_time']
        widgets = {
            'vehicle': forms.HiddenInput(),
            'start_time': DateTimePicker(
                options={
                    'useCurrent': False,
                    'minDate': timezone.now().strftime('%Y-%m-%d'),  
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),
            'end_time': DateTimePicker(
                options={
                    'useCurrent': False,
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        initial_vehicle = kwargs.pop('initial_vehicle', None)
        super().__init__(*args, **kwargs)
        if initial_vehicle:
            self.fields['vehicle'].initial = initial_vehicle

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < timezone.now():
            raise forms.ValidationError("Datum početka ne može biti u prošlosti.")
        return start_time