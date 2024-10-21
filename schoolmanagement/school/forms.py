from django import forms
from django.contrib.auth.models import User
from . import models

#Admin
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


#student
class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra
        fields = ['roll', 'cl', 'mobile', 'fee', 'status']


#teacher
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model = models.TeacherExtra
        fields = ['salary', 'mobile', 'status']



#Attendance
presence_choices = (('Present', 'Present'), ('Absent', 'Absent'))
class AttendanceForm(forms.Form):
    present_status = forms.ChoiceField(choices=presence_choices)
    date = forms.DateField()

class AskDateForm(forms.Form):
    date = forms.DateField()




#Notice
class NoticeForm(forms.ModelForm):
    class Meta:
        model = models.Notice
        fields = '__all__'



#contactus
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    