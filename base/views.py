from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q


#models import
from .models import Message, Post, Profile, Like, Comment

#forms import
from .forms import CommentForm, MessageForm, PostForm, CustomUserCreationForm, ProfileForm
# Create your views here.

@login_required(login_url='login_user')
def home(request, url_route):
    search_post = request.GET.get('post') if request.GET.get('post') != None else ''
    posts = Post.objects.filter(
        Q(owner__name__icontains=search_post) | 
        Q(owner__location__icontains=search_post)
    ).order_by('-created')
    latest_posts = Post.objects.all().order_by('-created')[0:4]
    user = request.user
    all_profiles = Profile.objects.all().order_by('-created')
    profile = Profile.objects.get(user=user)
    user_posts = Post.objects.filter(owner=profile).count()
    number_of_messages = Message.objects.filter(receiver = request.user.profile, mark_as_read = False).count()
    form = PostForm()
    comment_form = CommentForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = profile
            post.save()
            if url_route == 'home':
                return redirect('home', url_route='home')
            if url_route == 'user_account':
                return redirect('home', url_route='home')
            if url_route == 'user_profile':
                return redirect('user_profile', pk=profile.id)
    profile = Profile.objects.get(user=request.user)
    context = {
        'posts': posts,
        'latest_posts': latest_posts,
        'form': form,
        'url_route': 'home',
        'profile': profile,
        'user_posts': user_posts,
        'all_profiles': all_profiles,
        'comment_form': comment_form,
        'number_of_messages': number_of_messages,
    }
    return render(request, 'base/home.html', context)

@login_required(login_url='login_user')
def user_account(request):
    profile = Profile.objects.get(user=request.user)
    user_posts = Post.objects.filter(owner=profile).count()
    profile_form = ProfileForm(instance=profile)
    post_form = PostForm()
    if request.method == 'POST':
        cancel = request.POST.get('cancel')
        save= request.POST.get('save')
        if cancel:
            return redirect('home', url_route='home')
        if save:
            profile_form = ProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():
                profile_form= ProfileForm(request.POST, request.FILES, instance=profile)
                profile_form.save()
                return redirect('user_account')
    context = {
        'profile': profile,
        'profile_form': profile_form,
        'user_posts': user_posts,
        'url_route': 'user_account',
        'form': post_form
    }
    return render(request, 'base/account.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home', url_route='home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, '<p style="color: #fff; background-color: #ee5253;">Username does not exist</p>', extra_tags='safe')
            return redirect('home', url_route='home')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home', url_route='home')
        else:
            messages.error(request, '<p style="color: #fff; background-color: #ee5253;">Incorrect password</p>', extra_tags='safe')
            return redirect('home', url_route='home')
    return render(request, 'base/form-login.html')

def register_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, '<p style="color: #fff; background-color: #10ac84;">User account was created!</p>', extra_tags='safe')

            login(request, user)
            profile = Profile.objects.create(user=request.user, name=request.user.first_name, email=request.user.email)
            profile.save()
            return redirect('user_account')

        else:
            messages.success(
                request, '<p style="color: #fff; background-color: #ee5253;">An error has occurred during registration</p>', extra_tags='safe')

    context = {
        'form': form
    }
    return render(request, 'base/form-register.html', context)

@login_required(login_url='login_user')
def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    posts = profile.post_set.all().order_by('-created')
    user_posts = posts.count()
    post_form = PostForm()
    context = {
        'profile': profile,
        'posts': posts,
        'url_route': 'user_profile',
        'user_posts': user_posts,
        'form': post_form
    }
    return render(request, 'base/user-profile.html', context)

@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='login_user')
def delete_post(request):
    post_id = request.GET.get('id')
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        cancel = request.POST.get('cancel')
        confirm = request.POST.get('confirm')
        if cancel:
            return redirect('home', url_route='home')
        if confirm:
            post.image.delete()
            post.delete()
            return redirect('home', url_route='home')
    context = {
        'post': post
    }
    return render(request, 'base/post_delete.html', context)

@login_required(login_url='login_user')
def like_post(request, post_id, user_id):
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(id=user_id)

    liker = Like.objects.create(liker=profile)
    if liker.liker.id in [x.liker.id for x in post.likes.all()]:
        likers = Like.objects.filter(liker=profile)
        likers.delete()
    else:
        post.likes.add(liker)
    post.save()
    return redirect('home', url_route='home')

@login_required(login_url='login_user')
def comment_post(request, post_id, user_id):
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(id=user_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.commenter = profile
            comment.save()
            post.comments.add(comment)
            return redirect('home', url_route='home')

@login_required(login_url='login_user')
def following(request, user_id, following_user_id):
    user_profile = Profile.objects.get(id=user_id)
    following_user_profile = Profile.objects.get(id=following_user_id)
    user_profile.following.add(following_user_profile)
    following_user_profile.followers.add(user_profile)
    user_profile.save()
    following_user_profile.save()
    messages.success(
                request, '<p style="color: #fff; background-color: #10ac84;">You have started following {}</p>'.format(following_user_profile.name), extra_tags='safe')
    return redirect('home', url_route='home')

@login_required(login_url='login_user')
def message(request):
    all_profiles = Profile.objects.all().order_by('-created')
    post_form = PostForm()
    number_of_messages = Message.objects.filter(receiver = request.user.profile, mark_as_read = False).count()
    context = {
        'url_route': 'user_profile',
        'all_profiles': all_profiles,
        'form': post_form,
        'number_of_messages': number_of_messages,
    }
    return render(request, 'base/chat.html', context)

@login_required(login_url='login_user')
def chat_box(request, receiver_id):
    receiver = Profile.objects.get(id=receiver_id)
    all_profiles = Profile.objects.all().order_by('-created')
    post_form = PostForm()
    message_form = MessageForm()
    open_chat_box = True
    my_messages = Message.objects.filter(sender = request.user.profile, receiver = receiver).order_by('created')
    friend_messages = Message.objects.filter(sender = receiver, receiver = request.user.profile).order_by('created')
    number_of_messages = Message.objects.filter(receiver = request.user.profile, mark_as_read = False).count()
    number_of_friend_messages = Message.objects.filter(sender = receiver, receiver = request.user.profile, mark_as_read = False).count()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.receiver = receiver
            message.save()
            
            return redirect('chat_box', receiver_id=message.receiver.id) 
    context = {
        'url_route': 'user_profile',
        'all_profiles': all_profiles,
        'form': post_form,
        'receiver': receiver,
        'open_chat_box': open_chat_box,
        'message_form': message_form,
        'my_messages': my_messages,
        'friend_messages': friend_messages,
        'number_of_messages': number_of_messages,
        'number_of_friend_messages': number_of_friend_messages,
    }
    return render(request, 'base/chat.html', context)

@login_required(login_url='login_user')
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect('chat_box', receiver_id=message.receiver.id)
    
@login_required(login_url='login_user')
def mark_message_read(request, receiver_id):
    receiver = Profile.objects.get(id=receiver_id)
    number_of_friend_messages = Message.objects.filter(sender = receiver, receiver = request.user.profile, mark_as_read = False)
    for msg in list(number_of_friend_messages):
        msg.mark_as_read = True
        msg.save()
    return redirect('chat_box', receiver_id=receiver.id)





