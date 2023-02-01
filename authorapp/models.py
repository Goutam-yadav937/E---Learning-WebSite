from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class AuthorCourseListModelClass(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)    
    course_name  = models.CharField(max_length=20)
    


class AuthorCourseDataModalClass(models.Model):
    rel = models.ForeignKey(AuthorCourseListModelClass,on_delete=models.CASCADE)
    name = models.CharField(max_length = 15)
    discription = RichTextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)