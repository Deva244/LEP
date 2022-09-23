from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

account_types = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('manager', 'Manager')
]

class UserRegisterForm(UserCreationForm):
    first_name   = forms.CharField()
    last_name    = forms.CharField()
    email        = forms.EmailField()
    account_type = forms.CharField(label='Account Type: ', widget= forms.Select(choices=account_types))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'account_type']

class UserUpdateForm(forms.ModelForm):
    first_name   = forms.CharField()
    last_name    = forms.CharField()
    email        = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image']
