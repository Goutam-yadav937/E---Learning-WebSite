from django.urls import path
from . import views

urlpatterns=[
path('search/',views.searchdataview,name='search'),
path('coursesearch/',views.searchcourseview,name='coursesearch'),
]