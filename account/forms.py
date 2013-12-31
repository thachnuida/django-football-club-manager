from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models import UserProfile
from account.models import TITLE_CHOICES

class UserProfileForm(ModelForm):
  pos = forms.TypedChoiceField(widget=forms.Select(attrs={'class':'form-control', }),
                             choices=TITLE_CHOICES, )
  class Meta:
    model = UserProfile
    fields = ('pos', 'num', 'contact', 'avatar')
    widgets = {
      'num':forms.TextInput(attrs={'class':'form-control', }),
      'avatar':forms.FileInput(),
      'contact':forms.TextInput(attrs={'class':'form-control', }),
    }

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email')
    widgets = {
      'first_name':forms.TextInput(attrs={'class':'form-control', }),
      'last_name':forms.TextInput(attrs={'class':'form-control', }),
      'email':forms.TextInput(attrs={'class':'form-control','type':'email', }),
    }

class RegisterForm(UserCreationForm):
  username = forms.CharField()
  password1 = forms.CharField(label="Password")
  password2 = forms.CharField(label="Password confirmation")
  class Meta:
    model = User
    fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', )
    widgets = {
        'email':forms.TextInput(attrs={'class':'form-control','type':'email', }),
    }
