from django.contrib import admin
from .models import Post, Profile, Like, Comment, Message

# Register your models here.

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Message)