from django.contrib import admin
from django.urls import path, include

from main import views

urlpatterns = [
    path('dashboard', views.index, name="home"),
    path('', views.LandingPage, name="landingpage"),
]
