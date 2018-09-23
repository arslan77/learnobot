from django.contrib import admin
from django.urls import path, include

from Course import views
from Course.views import QuizViews, CourseViews

urlpatterns = [
    path('/dashboard', CourseViews.index, name="Index"),
    path('/<int:courseId>', CourseViews.CourseSelected, name="courseselected"),
    path('/<int:CourseId>/<int:CurrentCourseWorkId>', CourseViews.NextCourseWork, name="NextCourseWork"),
    path('/submit', CourseViews.SubmitQuizAnswer, name="SubmitQuizAnswer"),
    path('/result', QuizViews.ViewQuizResult, name="quizResult"),

]
