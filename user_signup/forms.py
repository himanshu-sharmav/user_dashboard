from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type=forms.CharField(widget=forms.RadioSelect(choices=[('doctor','Doctor'),('patient','Patient')]))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','confirm_password', 'profile_picture', 'address_line1', 'city', 'state', 'pin_code','first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password and Confirm Password should match')
        user_type = cleaned_data.get('user_type')
        if user_type not in ['doctor', 'patient']:
            raise forms.ValidationError('Invalid User Type')


# class UserLoginForm(AuthenticationForm):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
