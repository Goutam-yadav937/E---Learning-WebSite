from django.db import models
from django.contrib.auth.models import User

class CourseListClass(models.Model):
    course_name = models.CharField(max_length=20,null=True)
    course_discription = models.CharField(max_length=100,null=True)
    

    def __str__(self):
        return self.course_name


class UserProfileModelClass(models.Model):
    reluser = models.OneToOneField(User,on_delete = models.CASCADE,null=True)
    user_bio = models.TextField(max_length=200,null=True)


class BugReportModelClass(models.Model):
    report  = models.CharField(max_length=100)
    username  = models.CharField(max_length=100,null = True)
    date  = models.DateTimeField(auto_now_add=True)