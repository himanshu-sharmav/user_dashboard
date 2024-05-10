from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from .forms import UserSignupForm,BlogPostForm,AppointmentForm
from .models import BlogPost,BlogCategory,CustomUser,Appointment
from datetime import timedelta,time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os
import datetime
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            # user = authenticate(username=user.username, password=form.cleaned_data.get('password'))  # Corrected authentication
            user_type = form.cleaned_data['user_type']
            if user_type == 'patient':
                user.is_patient = True
            elif user_type == 'doctor':
                user.is_doctor = True
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserSignupForm()
    return render(request, 'user_signup/signup.html', {'form': form})        

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'Username: {username}')  # Print the username to the console
        print(f'Password: {password}')  # Print the password to the console
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:  # Check if the user is authenticated
                print('User is authenticated')  
            return redirect('dashboard')
        else:
            return render(request, 'user_signup/login.html', {'error': 'Invalid username or password'})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'user_signup/login.html')

def dashboard(request):
    # form=UserSignupForm() 
    if request.user.is_authenticated:
        user = request.user
        form = UserSignupForm(initial={'user_type': 'doctor' if user.is_doctor else 'patient'})
        if user.is_doctor:
            all_blogs = BlogPost.objects.filter(author=user)

            # Separate drafts from published blogs
            draft_blogs = all_blogs.filter(is_draft=True)
            published_blogs = all_blogs.filter(is_draft=False)

            return render(request, 'user_signup/dashboard.html', {'user': user, 'draft_blogs': draft_blogs, 'published_blogs': published_blogs, 'form': form})
        else:
            blog_posts = BlogPost.objects.filter(is_draft=False)
            return render(request, 'user_signup/dashboard.html', {'user': user, 'blog_posts': blog_posts, 'form': form})
    else:
        return redirect('login')  

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'user_signup/create_blog_post.html', {'form': form})

def view_blog_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'user_signup/view_blog_post.html', {'post': post})

def view_all_blog_posts(request):
    categories = BlogPost.objects.values_list('category__name', flat=True).distinct()
    categorized_posts = [(category, BlogPost.objects.filter(category__name=category, is_draft=False)) for category in categories]
    return render(request, 'user_signup/view_all_blog_posts.html', {'categorized_posts': categorized_posts})


def logout_view(request):
    logout(request)
    return redirect('login')

def doctor_list(request):
    doctors = CustomUser.objects.filter(is_doctor=True)
    return render(request, 'user_signup/doctor_list.html', {'doctors': doctors})

def book_appointment(request, doctor_id):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = CustomUser.objects.get(id=doctor_id)
            today = datetime.datetime.today().date()

# Convert appointment.start_time to a datetime
            start_datetime = datetime.datetime.combine(today, appointment.start_time)

# Now you can add the timedelta
            end_datetime = start_datetime + timedelta(minutes=45)

# And convert back to a time
            appointment.end_time = end_datetime.time()
            # appointment.end_time = appointment.start_time + timedelta(minutes=45)
            appointment.save()
            create_google_calender_event(appointment)
            return redirect('appointment_details', appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'user_signup/book_appointment.html', {'form': form})

def appointment_details(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'user_signup/appointment_details.html', {'appointment': appointment})

def create_google_calender_event(appointment):
    SCOPES=['https://www.googleapis.com/auth/calendar.events']
    creds =None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            flow.server.shutdown()    

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Appointment with ' + appointment.doctor.first_name + ' ' + appointment.doctor.last_name,
        'description': 'Appointment with ' + appointment.doctor.first_name + ' ' + appointment.doctor.last_name,
        'start': {
            'dateTime': appointment.date.isoformat() + 'T' + appointment.start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (appointment.date + datetime.timedelta(hours=appointment.start_time.hour, minutes=appointment.start_time.minute + 45)).isoformat()  + 'T' + appointment.start_time.isoformat(),
            'timeZone': 'UTC',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
