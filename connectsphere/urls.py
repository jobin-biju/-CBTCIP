from django.contrib import admin
from django.urls import path
from connectsphere import views
from django.contrib.auth import views as auth_views
from .views import homepage, like_post, add_comment
from django.conf import settings
from django.conf.urls.static import static
from .views import profile_view
from .views import message_page, chat_view, send_message, fetch_messages


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('homepage/', homepage, name='homepage'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', add_comment, name='add_comment'),
    path('profile/', profile_view, name='profile'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('profile_view_home/<str:email>/', views.profile_view_home, name='profile_view_home'),
    path('messages/', message_page, name='messages'),
    path('chat/<int:user_id>/', chat_view, name='chat'),
    path('send_message/', send_message, name='send_message'),
    path('fetch_messages/<int:user_id>/', fetch_messages, name='fetch_messages'),
    path('logout/', views.logout, name='logout'),
    path('update_password/', views.update_password, name='update_password'),
    path('notifications/', views.notifications, name='notifications'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),




    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
