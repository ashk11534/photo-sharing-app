from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=500)
    profile_image = models.ImageField(default='user-images/avatar.png', upload_to='user-images/')
    following = models.ManyToManyField('Profile', related_name='follow_to')
    followers = models.ManyToManyField('Profile', related_name='my_followers')
    location = models.CharField(max_length=200, null=True, blank=True)
    social_facebook = models.CharField(max_length=400, null=True, blank=True)
    social_linkedin = models.CharField(max_length=400, null=True, blank=True)
    social_twitter = models.CharField(max_length=400, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post-images/')
    likes = models.ManyToManyField('Like')
    comments = models.ManyToManyField('Comment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # def __str__(self):
    #     return 

class Like(models.Model):
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.liker.name

class Comment(models.Model):
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.commenter.name

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='message_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message_receiver')
    body = models.TextField(null=True, blank=True)
    mark_as_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)



