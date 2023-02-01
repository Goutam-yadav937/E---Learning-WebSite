from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import CourseListDataClass,UserRequestModelClass,CommentClass
from .forms import CourseListDataFormClass,UserRequestFormClass
from django.core.paginator import Paginator
from django.contrib import messages
from homeapp.models import CourseListClass,UserProfileModelClass
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User,Group

print(Paginator)
def coursedataview(request,id,name):
    data = CourseListDataClass.objects.filter(course=id).order_by('id')
    page = Paginator(data,10)
    number = request.GET.get('page')
    page_obj = page.get_page(number)
    context = {'page_obj':page_obj,'course':name,'courseid':id}
    return render(request,'coursedataapp/data.html',context)



def coursedataaddingview(request,id):
    if request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST['video_name']
            url = request.POST['video_url']
            discription = request.POST['video_discription']
            CourseListDataClass.objects.create(video_name=name,
            video_url=url,video_discription=discription,course_id=id)
            messages.info(request,f'adding done for course {CourseListClass.objects.get(id=id)}')
            return HttpResponseRedirect('/')
        else:    
            form = CourseListDataFormClass()
            return render(request,'coursedataapp/addingdata.html',{'form':form,'id':id})
    else:
        return HttpResponseRedirect('/')


############ showing video ##################
def videodataview(request,id):
    data = CourseListDataClass.objects.get(id=id)
    comments = CommentClass.objects.filter(video = data).order_by("-id")
    context = {'data':data,'comments':comments,'number':comments.count()}
    return render(request,'coursedataapp/videodata.html',context)


#################### storing parent comment from video comments ###############
def storeparentcommentsview(request,id):
    if request.method=="POST":
        user = request.user
        video = CourseListDataClass.objects.get(id=id)
        com = request.POST.get('comment')[:100]
        try:
            comment = CommentClass(user=user,video=video,com=com)
        except Exception:
            comment = CommentClass(user=None,video=video,com=com)
        comment.save()
        messages.info(request,'commented successfly')
        return HttpResponseRedirect(f'/coursedata/video/{id}')
    else:
        return HttpResponseRedirect(f'/coursedata/video/{id}')

#####################storing child comments from video comments ##########################

def storechildcommentsview(request,video_id,parent_id):
    if request.method=="POST":
        user = request.user
        video = CourseListDataClass.objects.get(id=video_id)
        com = request.POST.get('comment')[:100]
        parent = CommentClass.objects.get(id=parent_id)
        try:
            comment = CommentClass(user=user,video=video,com=com,parent=parent)
        except Exception:
            comment = CommentClass(user=None,video=video,com=com,parent=parent)
        comment.save()
        messages.info(request,'Replyed successfly')
        return HttpResponseRedirect(f'/coursedata/video/{video_id}')
    else:
        return HttpResponseRedirect(f'/coursedata/video/{video_id}')












@method_decorator(staff_member_required,name='dispatch')
class VideoDataEditClass(UpdateView):
    model = CourseListDataClass
    form_class = CourseListDataFormClass
    template_name = 'coursedataapp/videodataedit.html'
    success_url = '/'


def userrequestview(request):
    if request.method == 'POST':
        try:
            user = request.user
            Answer = request.POST.get('Answer')
            if user.groups.filter(name='Author').exists():
                messages.success(request,'You are already an Author..')
                return HttpResponseRedirect('/coursedata/userrequest/')
            else:
                obj = UserRequestModelClass(user=user,Answer=Answer)
                obj.save()
                messages.success(request,'requested')
                return HttpResponseRedirect('/')
        except Exception:
            messages.success(request,'You have already requested wait for admin\'s response')
            return HttpResponseRedirect('/coursedata/userrequest/')
    else:
        form = UserRequestFormClass()
        return render(request,'coursedataapp/userrequest.html',{'form':form})


class AllRequestForAuthorClass(ListView):
    model = UserRequestModelClass
    template_name = 'coursedataapp/authrequest.html'
    context_object_name = 'data'

    def get_queryset(self):
        return super().get_queryset().order_by('-id')



############ adding in group ########################


def addingauthor(request,name):
    if request.user.is_superuser:
        try:
            user = User.objects.get(username=name)
            group = Group.objects.get(name = 'Author')
            user.groups.add(group)
            UserRequestModelClass.objects.filter(user = user ).delete()
            messages.info(request,f'now {user} is an Author ')
            return HttpResponseRedirect('/coursedata/alluserrequestdata/')
        except Exception:
            messages.info(request,'Failed !')
            return HttpResponseRedirect('/coursedata/alluserrequestdata/')
    else:
        return HttpResponseRedirect('/')



################# retriving Author group's users##################
def authorpageview(request):
    id_number = Group.objects.get(name='Author')
    data = User.objects.filter(groups__in=[id_number])
    return render(request,'coursedataapp/authorspage.html',{'data':data})



################### rejecting Author group request#########################
def deleteauthorrequest(request,id):
    if request.user.is_superuser:    
        if request.method == 'POST':    
            try:
                obj = UserRequestModelClass.objects.get(id=id)
                obj.delete()
                messages.info(request,'Request Deleted')
                return HttpResponseRedirect('/coursedata/alluserrequestdata/')
            except:
                messages.info(request,'Failed !')
                return HttpResponseRedirect('/coursedata/alluserrequestdata/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')