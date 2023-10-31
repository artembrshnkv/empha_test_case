from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import ReservedRoom


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class BookRoomForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.product_id = kwargs.pop('number_id', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = ReservedRoom
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
            'number': forms.HiddenInput,
            'start_reservation': DatePickerInput(),
            'end_reservation': DatePickerInput(),
        }


class SortByDateForm(forms.Form):
    start_reservation = forms.DateField()
    end_reservation = forms.DateField()

    class Meta:
        fields = ['start_reservation', 'end_reservation']
        widgets = {
            'start_reservation': DatePickerInput(),
            'end_reservation': DatePickerInput()
        }

