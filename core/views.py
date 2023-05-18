from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount
from django.contrib.auth.decorators import login_required
from comments.models import Comment
from itertools import chain
import random


# Create your views here.
@login_required(login_url='login')
def index(request):
    user_object = request.user  # Use request.user directly
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user)

    for user in user_following:
        user_following_list.append(user.user)

    for user in user_following_list:
        feed_lists = Post.objects.filter(user=user)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))
    number_of_posts = len(feed_list)

    # user suggestion
    all_users = User.objects.all()
    user_following_all = [user.user for user in user_following]

    new_suggestion_list = [user for user in all_users if user not in user_following_all and user != request.user]
    random.shuffle(new_suggestion_list)

    suggestions_username_profile_list = Profile.objects.filter(user__in=new_suggestion_list)[:4]

    return render(request, 'core/index.html', {
        'user_profile': user_profile,
        'posts': feed_list,
        'number_of_posts': number_of_posts,
        'suggestions_username_profile_list': suggestions_username_profile_list,
    })

@login_required(login_url='login')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect(setting)

    return render(request, 'core/setting.html', {'user_profile': user_profile})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and direct to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user)

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password does not match')
            return redirect('signup')
    else:
        return render(request, 'core/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    else:
        return render(request, 'core/signin.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('index')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('index')

@login_required(login_url='login')
def profile_page(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(id=user_object.id)
    user_post_length = len(user_posts)

    follower = request.user.id
    user = user_object.id

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'

    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=user))
    user_following = len(FollowersCount.objects.filter(follower=user))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'core/profile.html', context)

@login_required(login_url='login')
def follow_user(request):
    if request.method == 'POST':
        follower_id = request.POST['follower']
        user_id = request.POST['user']

        follower = User.objects.get(id=follower_id)
        user = User.objects.get(id=user_id)

        follow_filter = FollowersCount.objects.filter(user=user, follower=follower).first()

        if follow_filter == None:
            new_follower = FollowersCount.objects.create(user=user, follower=follower)
            new_follower.save()
            return redirect('/profile/'+user.username)
        else:
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user.username)

    else:
        return redirect('/')

@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

    context = {
        'user_profile': user_profile,
        'username_profile_list': username_profile_list
    }
    return render(request, 'core/search.html', context)

