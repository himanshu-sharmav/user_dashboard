from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from .forms import UserSignupForm


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
      # replace 'login_view' with the name of your login view
    # print(request.user)
    return render(request, 'user_signup/dashboard.html', {'user': request.user})           
def logout_view(request):
    logout(request)
    return redirect('login')