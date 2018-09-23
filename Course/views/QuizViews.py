import json
from builtins import object

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from Course.models import Course, CourseWork, Quiz
from main.models import MyCourse, MyQuiz, MyQuizDetail


@login_required()
def ViewQuizResult(request):

    mineQuizez = MyQuiz.objects.filter(user=request.user).all()
    data = []
    counter = 1
    for quiz in mineQuizez:
        data.append(QuizVM(counter, quiz.course_work.course.course_name, quiz.course_work.work_name, quiz.total_marks, quiz.obtained_marks, quiz.is_finish, quiz.start_time))
        counter = counter + 1
    return render(request, 'course/QuizResult.html', {"quizez":data})




class QuizVM:
    def __init__(self, id=0, subjectName='',quizName = '', totalMarks = 0, obtainedMarks = 0, is_finish=False, dateTime = timezone.now()):
        self.Id = id
        self.SubjectName = subjectName
        self.QuizName = quizName
        if totalMarks is not None:
            self.TotalMarks = totalMarks
        else:
            self.TotalMarks = 0
        if obtainedMarks is not None:
            self.ObtainedMarks = obtainedMarks
        else:
            self.ObtainedMarks = 0
        if is_finish:
            self.is_completed = "Completed"
        else:
            self.is_completed = "Under Process"
        # if dateTime is None:
        #     self.DateTime = timezone.now()
        # else:
        self.DateTime = dateTime
        self.Percentage = round(self.CalculatePercentage(), 2)
        self.ClassName = self.GetClassName()
    def CalculatePercentage(self):
        if(self.ObtainedMarks==0 | self.TotalMarks==0):
            return 0
        return (self.ObtainedMarks/self.TotalMarks)*100.00

    def GetClassName(self):
        if self.Percentage < 50:
            return "label-danger"
        elif self.Percentage<70:
            return "label-warning"
        elif self.Percentage <85:
            return "label-primary"
        else:
            return "label-success"