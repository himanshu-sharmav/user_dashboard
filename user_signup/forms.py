from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser,BlogPost,BlogCategory,Appointment
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

CATEGORY_CHOICES = [
    ('Mental Health', 'Mental Health'),
    ('Heart Disease', 'Heart Disease'),
    ('Covid19', 'Covid19'),
    ('Immunization', 'Immunization'),
]
class BlogPostForm(forms.ModelForm):
    # category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    class Meta:
        model= BlogPost
        fields=['title','image','category','summary','content','is_draft']
    # category = forms.CharField(widget=forms.Select(choices=CATEGORY_CHOICES))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = BlogCategory.objects.all()
# class UserLoginForm(AuthenticationForm):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d-%m-%Y'])
    class Meta:
        model = Appointment
        fields = ['speciality','date','start_time']   