from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from coursedataapp.models import CourseListDataClass
from authorapp.models import AuthorCourseListModelClass,AuthorCourseDataModalClass
from django.http import Http404
from django.core.paginator import Paginator



def searchdataview(request):
    dt = request.GET.get('searchdata')
    if (len(dt)<=80): 
        data1 = CourseListDataClass.objects.filter(video_name__icontains = dt) 
        data2 = CourseListDataClass.objects.filter(video_discription__icontains = dt)
        data_a = data1.union(data2)
        data3 = AuthorCourseDataModalClass.objects.filter(name__icontains = dt) 
        data4 = AuthorCourseDataModalClass.objects.filter(discription__icontains = dt)
        data_b = data3.union(data4)
    else:
        data_a = None
        data_b = None
        
    context = {'answer1':data_a,'answer2':data_b,'searchdata':dt}
    return render(request,'searchapp/search.html',context)





'''
the below code is to provide a search facility in more courses section
in whicth we are showing the authors courses 
'''
def searchcourseview(request):
    search = request.GET.get('searchcoursedata')
    if (len(search) != 0):    
        data = AuthorCourseListModelClass.objects.filter(course_name__icontains = search).order_by('course_name')
        pg = Paginator(data,1000000000)
        number = request.GET.get('page')
        page_obj = pg.get_page(number)
        context = {'page_obj':page_obj,'query':search}
        return render(request,'authorapp/alldatashow.html',context)
    else:
        return HttpResponseRedirect('/authorpage/allcourses/')


