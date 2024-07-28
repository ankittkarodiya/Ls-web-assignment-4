from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# new
from django.utils import timezone
from .models import Tweet
from .forms import TweetForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"User registered: {user.username}")  # Debugging line
            return redirect('django_app:home')
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = RegisterForm()
    return render(request, "django_app/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('django_app:home')  
    else:
        form = AuthenticationForm()
    return render(request, "django_app/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('django_app:login')  

@login_required
def profile(request):
    # return render(request, 'django_app/profile.html')
    return render(request, 'django_app/profile.html', {'user': request.user})


@login_required
def home_view(request):
    return render(request, "django_app/home.html")


# new
@login_required
def create_tweet(request):
    if request.method == "POST":
        content = request.POST.get('content')
        media = request.FILES.get('media')

        Tweet.objects.create(user=request.user, content=content)
        return redirect('django_app:tweet_list')
    return render(request, 'django_app/create.html')

@login_required
def tweet_list(request):
    tweets = Tweet.objects.all()
    return render(request, 'django_app/tweet_list.html', {'tweets': tweets})

# @login_required
# def tweet_list_view(request):
#     tweets = Tweet.objects.all().order_by('-created_at')
#     return render(request, 'django_app/tweets.html', {'tweets': tweets})

@login_required
def post_tweet_view(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.created_at = timezone.now()
            tweet.save()
            return redirect('django_app:tweet_list')
    else:
        form = TweetForm()
    return render(request, 'django_app/create.html', {'form': form})

@login_required
def delete_tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user == tweet.user:
        tweet.delete()
    return redirect('django_app:tweet_list')

@login_required
# def edit_tweet_view(request, tweet_id):
#     tweet = get_object_or_404(Tweet, id=tweet_id)
#     if request.user != tweet.user:
#         return redirect('django_app:tweet_list')
#     if request.method == 'POST':
#         form = TweetForm(request.POST, request.FILES, instance=tweet)
#         if form.is_valid():
#             form.save()
#             return redirect('django_app:tweet_list')
#     else:
#         form = TweetForm(instance=tweet)
#     return render(request, 'django_app/create.html', {'form': form})

def edit_tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == 'POST':
        tweet.content = request.POST.get('content')
        if request.FILES.get('media'):
            tweet.media = request.FILES.get('media')
        tweet.save()
        return redirect('django_app:tweet_list')
    return render(request, 'django_app/edit_tweet.html', {'tweet': tweet})

