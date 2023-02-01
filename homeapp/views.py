from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .forms import RegistrationForm,LoginForm,CourseListFormClass,UserbioFormClass,Change_Password
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from .models import CourseListClass,UserProfileModelClass,BugReportModelClass
from django.contrib.auth.models import User
from django.core.cache import cache

def home(request):
    signupform = RegistrationForm() # Registration Form 
    loginform = LoginForm() # Login Form
    coursedata = CourseListClass.objects.order_by('id') # coursedata retriving 
    courseform = CourseListFormClass()#course adding form
    
    total={'signupform':signupform,'loginform':loginform,'totalcoursedata':coursedata,
    'courseform':courseform}
    return render(request,'homeapp/homepage.html',total)


######################## Course Data Adding #############################

def coursedataaddingview(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            data = CourseListFormClass(request.POST)
            if data.is_valid():
                data.save()
                messages.info(request,'adding done')
                return HttpResponseRedirect('/')
            else:
                messages.info(request,'not valid')
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


################ Authentication system coding below ###################
def registrationview(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        data = RegistrationForm(request.POST)
        if data.is_valid():
            data.save()
            username = data.cleaned_data['username']
            password = data.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                messages.info(request,"you are registered in our website please login mannuly")
                return HttpResponseRedirect('/')
        else:
            messages.info(request,"1.username is taken. or 2.passwords dosn't match.")
            return HttpResponseRedirect('/')

def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request,'logged out!')
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def loginview(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:            
        data = LoginForm(request.POST)
        if data.is_valid():
            username = data.cleaned_data['username']
            password = data.cleaned_data['password']
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                messages.info(request,"1.you don't have any account. or 2.you entered wrong input")
                return HttpResponseRedirect('/')
        else:
            messages.info(request,"1.you don't have any account. or 2.you entered wrong input")
            return HttpResponseRedirect('/')

                
def profileview(request):
    if request.user.is_authenticated:
        user_data_1 = request.user
        flag = user_data_1.groups.filter(name='Author').exists()
        
        try:
            user_data_2 = UserProfileModelClass.objects.get(reluser_id=user_data_1)
        except Exception:
            user_data_2 = None
        return render(request,'homeapp/profile.html',{'user1':user_data_1,
        'user2':user_data_2,'flag':flag})
    else:
        messages.info(request,'First login to unlock this feature,Thankyou!')
        return HttpResponseRedirect('/')


def authorprofileview(request,author):
    user_data_1 = User.objects.get(id=author)
    if user_data_1.groups.filter(name='Author').exists():    
        try:
            user_data_2 = UserProfileModelClass.objects.get(reluser_id=author)
        except Exception:
            
            user_data_2 = None
        return render(request,'homeapp/authorprofile.html',{'user1':user_data_1,'user2':user_data_2})
    else:
        messages.info(request,"Don\'t try to be over smart !")
        return HttpResponseRedirect('/')


def settingsview(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            obj = UserProfileModelClass.objects.get(reluser_id = user)
        except Exception:
            obj = None
        form1 = UserbioFormClass(instance = obj)
        form2 = Change_Password(user=request.user)
        return render(request,'homeapp/settings.html',{'form1':form1,'form2':form2})
    else:
        messages.info(request,'First login to unlock this feature,Thankyou!')
        return HttpResponseRedirect('/')

##################### changing user bio ##################################
def editbioview(request):
    if request.user.is_authenticated:
        user = request.user
        bio = request.POST['user_bio'][:80]
        if UserProfileModelClass.objects.filter(reluser_id = user).exists():
            UserProfileModelClass.objects.filter(reluser_id = user).update(user_bio = bio)
            messages.info(request,'your bio is updated !')
            return HttpResponseRedirect('/settings/')
        else:
            UserProfileModelClass.objects.create(user_bio = bio,reluser = user)
            messages.info(request,'thanks for adding your bio !')
            return HttpResponseRedirect('/settings/')
    else:
        return HttpResponseRedirect('/')

#################### changing user password ########################
def changepasswordview(request):
    if request.method=='POST':
        dt = Change_Password(user=request.user,data=request.POST)
        if dt.is_valid():
            dt.save()
            update_session_auth_hash(request,dt.user)
            messages.info(request,'your password is changed')
            return HttpResponseRedirect('/settings/')
        else:
            messages.info(request,'your input is not valid try again ')
            return HttpResponseRedirect('/settings/')
    else:
        return HttpResponseRedirect('/')

#######################################################################

def authorpannel(request):
    if request.user.is_superuser:
        return render(request,'homeapp/adminpannel.html')
    else:
        return HttpResponseRedirect('/')

#################### clearing_cached_data #####################

def clearcachedata(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            cache.clear()
            messages.info(request,'clearing done')
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

################ bug report section ###############

def bugreportview(request):
    if request.method == 'POST':
        report = request.POST.get('reportbug')
        username = request.user
        BugReportModelClass.objects.create(report = report,username = username)
        messages.info(request,'Thanks for reporting ')
        return HttpResponseRedirect('/report/')
    else:
        data = BugReportModelClass.objects.all().order_by("-id")
        return render(request,'homeapp/bugreport.html',{'data':data})

########### deleting the reports ########### by superuser only ############ 
def bugreportdeleteview(request,id):
    if request.user.is_superuser:
        if request.method == 'POST':
            obj = BugReportModelClass(id=id)
            obj.delete()
            messages.info(request,'deleted')
            return HttpResponseRedirect('/report/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')