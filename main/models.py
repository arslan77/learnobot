
from django.db import models

# Create your models here.


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from Course.models import Course, CourseWork


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    designation = forms.CharField(max_length=40, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'designation' , 'first_name', 'last_name', 'email', 'password1', 'password2')

        def get_full_name(self):
            '''
            Returns the first_name plus the last_name, with a space in between.
            '''
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()



class MyCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_course_work = models.ForeignKey(CourseWork, on_delete=models.CASCADE, null=True, blank=True)
    course_completed = models.BooleanField(default=False)
    percentage = models.IntegerField(default=0)

class MyQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_work = models.ForeignKey(CourseWork, on_delete=models.CASCADE)
    obtained_marks = models.IntegerField(null=True, blank=True)
    total_marks = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_finish = models.BooleanField(default=False)

class MyQuizDetail(models.Model):
    myQuiz = models.ForeignKey(MyQuiz, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=5, null=True, blank=True)
    right_option = models.CharField(max_length=5, null=True, blank=True)
    is_right = models.BooleanField(default=False, null=True, blank=True)