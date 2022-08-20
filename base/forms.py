from django.forms import ModelForm
from .models import Comment, Message, Post, Profile, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image']
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'choose-button'})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user','following', 'followers')
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'shadow-none bg-gray-100'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.label = ''
            field.widget.attrs.update({'class': 'bg-transparent max-h-8 shadow-none', 'placeholder': 'Add your Comment...'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        labels = {
            'body': '',
        }
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.label = ''
            field.widget.attrs.update({'class': 'border-0 flex-1 h-10 min-h-0 resize-none min-w-0 shadow-none dark:bg-transparent', 'placeholder': 'Your Message...', 'cols': '1', 'rows': '1'})

        