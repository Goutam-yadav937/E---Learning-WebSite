from django.urls import path
from . import views
urlpatterns = [
    path('course/<int:id>/<str:name>/',views.coursedataview,name='courses'),
    path('courseadding/<int:id>/',views.coursedataaddingview,name='courseadding'),
    path('video/<int:id>/',views.videodataview,name='videodata'),
    path('pcomments/<int:id>/',views.storeparentcommentsview,name='parentcomments'),
    path('ccomments/<int:video_id>/<str:parent_id>/',views.storechildcommentsview,name='childcomments'),
    path('videoedit/<int:pk>/',views.VideoDataEditClass.as_view(),name='videodataedit'),
    path('userrequest/',views.userrequestview,name='userrequest'),
    path('alluserrequestdata/',views.AllRequestForAuthorClass.as_view(),name='alluserrequestdata'),
    path('addingauthor/<str:name>/',views.addingauthor,name='addingauthor'),
    path('deleteautherrequest/<int:id>/',views.deleteauthorrequest,name='deleteautherrequest'),
    path('authorpage/',views.authorpageview,name='authorpage'),
]