from django.contrib import admin
from .models import CourseListClass,UserProfileModelClass,BugReportModelClass

@admin.register(CourseListClass)
class CourseListAdminClass(admin.ModelAdmin):
    list_display = ['id','course_name','course_discription']

############### custom profile image for user register ###################
admin.site.register(UserProfileModelClass)

#################### bug report model regitering ################
@admin.register(BugReportModelClass)
class BugReportAdminClass(admin.ModelAdmin):
    list_display = ['id','report','username','date']