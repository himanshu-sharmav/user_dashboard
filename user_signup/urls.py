from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-blog/', views.create_blog_post, name='create_blog_post'),
    path('logout/', views.logout_view, name='logout_view'),
    path('view-blog-post/<int:post_id>/', views.view_blog_post, name='view_blog_post'),
    path('view-all-blog-posts/', views.view_all_blog_posts, name='view_all_blog_posts'),
    path('doctors/', views.doctor_list, name='list_doctors'),
    path('book-appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:appointment_id>/', views.appointment_details, name='appointment_details'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)