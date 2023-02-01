from django import forms
from .models import AuthorCourseListModelClass,AuthorCourseDataModalClass

class AuthorCourseListFormClass(forms.ModelForm):
    class Meta:
        model = AuthorCourseListModelClass
        fields = ['course_name']
        labels = {'course_name':' Course name'}
        widgets = {'course_name':forms.TextInput(attrs={'class':'form-control','placeholder':'course name'}),
                }

class AuthorCourseDataFormClass(forms.ModelForm):
    class Meta:
        model = AuthorCourseDataModalClass
        fields = ['name','discription']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'discription':forms.Textarea(attrs={'class':'form-control'})
        }