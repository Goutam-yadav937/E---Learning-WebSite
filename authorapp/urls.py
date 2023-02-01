from django.urls import path
from . import views

urlpatterns = [
    path('auth/',views.authorfeature,name='auth'),
    path('adding/<int:id>/',views.authorcoursedataview,name='adding'),
    path('datadelete/<int:data_id>/<int:course_id>/',views.authorcoursedatadeleteview,name='authordatadelete'),
    path('dataedit/<int:data_id>/<int:course_id>/',views.authorcoursedataeditview,name='authordataedit'),
    path('coursenamechange/<int:id>/',views.coursenamechangeview,name='coursenamechange'),
    path('coursedeleteby/<int:id>/',views.coursedeletebyview,name='coursedeleteby'),
    path('allcourses/',views.AllCourseDataClass.as_view(),name='allcourses'),
    path('coursetopics/<int:id>/',views.coursetopicview,name='coursetopics'),
    path('topic/<int:pk>/',views.TopicClass.as_view(),name='topic'),
]