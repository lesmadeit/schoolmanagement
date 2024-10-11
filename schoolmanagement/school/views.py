from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/index.html')



#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/adminclick.html')


#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/teacherclick.html')


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/studentclick.html')





def admin_signup_view(request):
    form = forms.AdminSignupForm()
    if request.method == 'POST':
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.ass(user)

            return HttpResponseRedirect('adminlogin')
    return render(request, 'school/adminsignup.html', {'form':form})




def student_signup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1':form1, 'form2':form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.passwords)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request, 'school/studentsignup.html', context=mydict)


def teacher_signup_view(request):
    form1 = forms.TeacherUserForm()
    form2 = forms.TeacherExtraForm()
    mydict = {'form1':form1, 'form2':form2}
    if request.method == 'POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request, 'school/teachersignup.html', context=mydict)




#for checking if user is teacher, student or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval = models.TeacherExtra.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request, 'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval = models.StudentExtra.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request, 'school/student_wait_for_approval.html')
        



#admin dashboard

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount = models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount = models.TeacherExtra.objects.all().filter(status=False).count()
    