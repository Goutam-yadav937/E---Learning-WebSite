from django.contrib import admin
from .models import CourseListDataClass ,UserRequestModelClass,CommentClass

@admin.register(CourseListDataClass)
class CourseListDataAdminClass(admin.ModelAdmin):
    list_display = ['id','course','video_name','video_url','video_discription','video_date']


@admin.register(UserRequestModelClass)
class UserRequestModelAdminClass(admin.ModelAdmin):
    list_display = ['id','user','Answer','date']


@admin.register(CommentClass)
class CommnetAdminClass(admin.ModelAdmin):
    list_display = ['id','user','video','com','parent','date']