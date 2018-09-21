from django.contrib import admin
from django.urls import path, include

from Course import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('<int:courseId>', views.CourseSelected, name="courseselected"),
    path('<int:CourseId>/<int:CurrentCourseWorkId>', views.NextCourseWork, name="NextCourseWork"),
    path('submit', views.SubmitQuizAnswer, name="SubmitQuizAnswer"),

]
