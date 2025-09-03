from django import forms
from django.forms import ModelForm
from CgpaApp.models import Register
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Reg(forms.ModelForm):
    class Meta:
        model=Register #db_name
        fields=['name','mobile_no','gender','branch']
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Name'}),
            'mobile_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Mobile Number'}),
            'gender':forms.RadioSelect(),
            'branch':forms.Select(attrs={'class':'form-control'})
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

