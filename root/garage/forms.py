from .models import Chat_post, Profile, Comments
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Chat_post
        fields = ['title', 'flair', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 text-white border border-gray-800 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-950',
                'placeholder': 'Enter a catchy title...'
            }),
            'flair': forms.Select(attrs={
                'class': 'w-1/4 px-1 py-1 border border-gray-800 rounded-lg shadow-sm bg-cyan-800 focus:outline-none focus:ring-2 focus:ring-cyan-950'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-800 rounded-lg shadow-sm h-32 resize-y focus:outline-none focus:ring-2 focus:ring-cyan-950',
                'placeholder': 'Write your thoughts here...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-cyan-900 file:text-white hover:file:bg-cyan-950'
            }),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 text-black border border-gray-800 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-950',
            'placeholder': 'Enter your email...'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 text-black border border-gray-800 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-950',
            'placeholder': 'Choose a username...'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 text-black border border-gray-800 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-950',
            'placeholder': 'Enter password...'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 text-black border border-gray-800 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-950',
            'placeholder': 'Confirm password...'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-cyan-900 file:text-white hover:file:bg-cyan-950'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment',]
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write a comment...',
                'class': 'px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none dark:text-white dark:placeholder-gray-400 dark:bg-gray-800'
            })
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment',] 
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Write your reply...',
                'class': 'px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none dark:text-white dark:placeholder-gray-400 dark:bg-gray-800',
            }),
        }
