from django.db import models
from homeapp.models import CourseListClass
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User



class CourseListDataClass(models.Model):
    course = models.ForeignKey(CourseListClass,on_delete=models.CASCADE)
    video_name = models.CharField(max_length=100)
    video_url = models.CharField(max_length=200,null=True)
    video_discription = RichTextField(blank=True,null=True)
    video_date = models.DateTimeField(default=now)


class UserRequestModelClass(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Answer = models.TextField(max_length=300,null=True)
    date = models.DateTimeField(default=now)


class CommentClass(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    video = models.ForeignKey(CourseListDataClass,on_delete=models.CASCADE)
    com = models.CharField(max_length=100)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    date = models.DateField(default=now)

