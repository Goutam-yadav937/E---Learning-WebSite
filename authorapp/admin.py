from django.contrib import admin
from .models import AuthorCourseListModelClass,AuthorCourseDataModalClass


@admin.register(AuthorCourseListModelClass)
class AuthorCourseListAdminClass(admin.ModelAdmin):
    list_display = ['id','user','course_name']


@admin.register(AuthorCourseDataModalClass)
class AuthorCourseDataAdminClass(admin.ModelAdmin):
    list_display = ['id','rel','name','discription','date']
