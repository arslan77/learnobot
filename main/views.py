from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Course.models import Course
from main.models import SignUpForm, MyCourse


@login_required
def index(request):
    courses = Course.objects.all()
    for course in courses:
        course.myCourse = MyCourse.objects.filter(user=request.user, course=course).first()

    # print(courses[1].myCourse)
    return render(request, 'index.html', {
        'courses': courses,
    })


def LandingPage(request):
    return render(request, 'landingpage.html')



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})