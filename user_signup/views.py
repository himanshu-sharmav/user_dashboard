from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from .forms import UserSignupForm,BlogPostForm
from .models import BlogPost,BlogCategory


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
            blog_posts = BlogPost.objects.filter(author=user)
            return render(request, 'user_signup/dashboard.html', {'user': user, 'blog_posts': blog_posts, 'form': form})
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