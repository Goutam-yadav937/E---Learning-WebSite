from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import AuthorCourseListModelClass,AuthorCourseDataModalClass
from .forms import AuthorCourseListFormClass,AuthorCourseDataFormClass
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404
'''
by the below method we are storing the Author courses and fetching the user create
courses according to user you know what i mean 
'''
def authorfeature(request):
    if request.user.groups.filter(name = 'Author').exists():
        if request.method=='POST':
                data = AuthorCourseListFormClass(request.POST)
                if data.is_valid():
                    user = request.user
                    name = data.cleaned_data['course_name']
                    AuthorCourseListModelClass.objects.create(user=user,course_name=name)
                    messages.info(request,f' \'{name}\' course added ')
                    return HttpResponseRedirect('/authorpage/auth/')
                else:
                    messages.info(request,'sorry your data is not valid')
                    return HttpResponseRedirect('/authorpage/auth/')
        else:    
            list_form = AuthorCourseListFormClass()
            data = AuthorCourseListModelClass.objects.filter(user = request.user)
            context = {'list_form':list_form,'data':data}
            return render(request,'authorapp/addingdatabyauthor.html',context)
    else:
        messages.info(request,'this feature is only available for Authors')        
        return HttpResponseRedirect('/')



'''
in below code we are storing data of topics and showing to
respective author only so he will know what he created
'''
def authorcoursedataview(request,id):
    if request.user.groups.filter(name = 'Author').exists():
        if AuthorCourseListModelClass.objects.filter(id=id,user=request.user).exists():
            if request.method=='POST':
                rel = AuthorCourseListModelClass.objects.get(id=id)
                name = request.POST.get('name')
                dis = request.POST.get('discription')
                AuthorCourseDataModalClass.objects.create(rel=rel,name=name,discription=dis)
                messages.info(request,f'\'{name}\' added successfully')
                return HttpResponseRedirect(f'/authorpage/adding/{id}')
            else:
                form = AuthorCourseDataFormClass()
                obj = AuthorCourseListModelClass.objects.get(id=id)
                course_name_change_form = AuthorCourseListFormClass(instance=obj)
                rel = AuthorCourseListModelClass.objects.get(id=id)
                data = AuthorCourseDataModalClass.objects.filter(rel=rel)
                context = {'form':form,'id':id,'data':data,'course_form':course_name_change_form}
                return render(request,'authorapp/authorcoursedataadding.html',context)
        else:
            return HttpResponseRedirect('/authorpage/auth/')
    else:
        return HttpResponseRedirect('/')




'''
deleting the data of courses by authors to thier data 
'''
def authorcoursedatadeleteview(request,data_id,course_id):
    if request.user.groups.filter(name='Author').exists():
        if AuthorCourseListModelClass.objects.filter(id=course_id,user=request.user).exists():
            if request.method=='POST':
                obj = AuthorCourseDataModalClass.objects.get(id=data_id)
                obj.delete()
                messages.info(request,'deleted successfully')
                return HttpResponseRedirect(f'/authorpage/adding/{course_id}/')
            else:
                return HttpResponseRedirect('/')
        else:
            messages.info(request,'sorry access denied')
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')



'''
editing data of courses according to their Author only 
'''
def authorcoursedataeditview(request,data_id,course_id):
    if request.user.groups.filter(name='Author').exists():
        if AuthorCourseListModelClass.objects.filter(id=course_id,user=request.user).exists():
            if request.method=='POST':
                name = request.POST.get('name')
                dis = request.POST.get('discription')
                AuthorCourseDataModalClass.objects.filter(id=data_id).update(name=name,discription=dis)
                messages.info(request,'updated successfully')
                return HttpResponseRedirect(f'/authorpage/adding/{course_id}/')
            else:
                obj = AuthorCourseDataModalClass.objects.get(id=data_id)
                form = AuthorCourseDataFormClass(instance=obj)
                context = {'form':form}
                return render(request,'authorapp/coursedataedit.html',context)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')



'''        
in below code we will change the course name respectivly to author 
by validating him
'''
def coursenamechangeview(request,id):
    if request.user.groups.filter(name='Author').exists():
        if AuthorCourseListModelClass.objects.filter(id=id,user=request.user).exists():
            if request.method=='POST':
                name = request.POST.get('course_name')
                AuthorCourseListModelClass.objects.filter(id=id).update(course_name=name)
                messages.success(request,f'Course Name Changed To {name}')
                return HttpResponseRedirect('/authorpage/auth/')
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')



'''
in the below code Author Can delete his course and we will give him a alert
about all topics that will be deleted also thank you 
'''

def coursedeletebyview(request,id):
    if request.user.groups.filter(name='Author').exists():
        if AuthorCourseListModelClass.objects.filter(id=id,user=request.user).exists():
            if request.method=='POST':
                obj = AuthorCourseListModelClass.objects.get(id=id)
                obj.delete()
                messages.info(request,'Course deleted successfully')
                return HttpResponseRedirect('/authorpage/auth/')
            else:
                return render(request,'authorapp/coursedeleteby.html')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
 


'''
in the below code we are showing courses to users 
with pagination
'''
class AllCourseDataClass(ListView):
    model = AuthorCourseListModelClass
    template_name='authorapp/alldatashow.html'
    paginate_by=12

    def get_queryset(self):#this method is for ordering the data
        return super().get_queryset().order_by('course_name')

    def paginate_queryset(self, queryset, page_size,**kwargs):
        try:#this method is for page not found error to handle it   
            return super(AllCourseDataClass,self).paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page']=1
            return super(AllCourseDataClass,self).paginate_queryset(queryset,page_size)


#### showing course data according to course ################
def coursetopicview(request,id):
     obj = AuthorCourseListModelClass.objects.get(id=id)
     data = AuthorCourseDataModalClass.objects.filter(rel = obj)
     return render(request,'authorapp/coursedatatouser.html',{'data':data})


class TopicClass(DetailView):
    model = AuthorCourseDataModalClass
    template_name = 'authorapp/topic.html'
    context_object_name = 'data'
