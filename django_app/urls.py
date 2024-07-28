from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, home_view, profile, create_tweet, tweet_list, post_tweet_view, delete_tweet_view, edit_tweet_view


app_name = 'django_app'  # namespace

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('profile/', views.profile, name='profile'),

    # new
    path('create/', create_tweet, name='create_tweet'),
    path('tweet_list/', tweet_list, name='tweet_list'),
    path('tweet_list/post/', post_tweet_view, name='post_tweet'),
    path('tweet_list/delete/<int:tweet_id>/', delete_tweet_view, name='delete_tweet'),
    path('tweet_list/edit/<int:tweet_id>/', edit_tweet_view, name='edit_tweet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
