from django.urls import path
from . import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path('',views.home,name='home'),
    path('coursedataadding/',views.coursedataaddingview,name='coursedataadding'),
    path('signup/',views.registrationview,name='signup'),
    path('login/',views.loginview,name='login'),
    path('logout/',views.logoutview,name='logout'),
    path('profile/',views.profileview,name='profile'),
    path('author/<int:author>/',views.authorprofileview,name='author'),
    path('settings/',views.settingsview,name='settings'),
    path('editbio/',views.editbioview,name='editbio'),
    path('changepassword/',views.changepasswordview,name='changepassword'),
    path('authorpannel/',views.authorpannel,name='authorpannel'),
    path('clearcache/',views.clearcachedata,name='clearcache'),
    path('contect/',TemplateView.as_view(template_name='homeapp/contect.html'),name='contect'),
    path('report/',views.bugreportview,name='report'),
    path('deletereport/<int:id>/',views.bugreportdeleteview,name='deletereport'),
    
]