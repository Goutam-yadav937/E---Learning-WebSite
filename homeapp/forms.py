from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import CourseListClass,UserProfileModelClass


class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'@password'}))
    password2=forms.CharField(label='password(again)',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'@password'}))
    class Meta:
        model=User
        fields=('username','email')
        labels={'first_name':'First Name','last_name':'Last Name','email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control','placeholder':'xyz'}),
                'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'xyz@gmail.com'})}
        
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'xyz'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'@password'}))



class CourseListFormClass(forms.ModelForm):
    class Meta:
        model = CourseListClass
        fields='__all__'
        widgets={'course_name':forms.TextInput(attrs={'class':'form-control'}),
            'course_discription':forms.Textarea(attrs={'class':'form-control'})}    



class UserbioFormClass(forms.ModelForm):
    class Meta:
        model = UserProfileModelClass
        fields = ['user_bio']
        labels = {'user_bio':'Add bio'}
        widgets = {'user_bio':forms.Textarea(attrs={'class':'form-control'})}



class Change_Password(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
