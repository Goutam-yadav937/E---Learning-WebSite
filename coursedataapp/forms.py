from .models import CourseListDataClass,UserRequestModelClass
from django import forms



class CourseListDataFormClass(forms.ModelForm):
    class Meta:
        model = CourseListDataClass
        fields = ['video_name','video_url','video_discription']
        labels = {'video_name':'Name','video_url':'url','video_discription':'discription'}
        widgets = {'video_name':forms.TextInput(attrs={'class':'form-control',}),
        'video_url':forms.TextInput(attrs={'class':'form-control'}),
        'video_discription':forms.Textarea(attrs={'class':'form-control'}),}


class UserRequestFormClass(forms.ModelForm):
    
    class Meta:
        model = UserRequestModelClass
        fields = ['Answer']
        widgets = {'Answer':forms.Textarea(attrs={'class':'form-control color','placeholder':'Type here.....'})}
        