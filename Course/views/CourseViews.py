import json
from builtins import object

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from Course.models import Course, CourseWork, Quiz
from main.models import MyCourse, MyQuiz, MyQuizDetail


@login_required
def index(request):
    # print('Hy')
    # return HttpResponse("This sad be landing page.")
    test = ['1', 2,"three"]

    return render(request, 'index.html', {
        'foo': test,
    })

def CourseSelected(request, courseId=0):
    resp = {}
    resp["course"] = Course.objects.get(pk= courseId)
    resp["mineCourse"] = MyCourse.objects.filter(course__course_id=resp["course"].course_id , user=request.user).first()

    if resp["mineCourse"] is None:
        resp["mineCourse"] = MyCourse(user=request.user, course=resp["course"])
        resp["mineCourse"].save()

    if resp["mineCourse"].current_course_work is None:
        if (resp["course"].coursework_set.count() == 0):
            return render(request, 'extra/error.html', {
                'error_heading': 'No Course Work',
                'error_message': 'There is no course work for ' + resp["course"].__str__()
            })

        courseWork = resp["course"].coursework_set.all()
        resp["mineCourse"].current_course_work = courseWork.first()
        resp["mineCourse"].save()

    if resp["mineCourse"].percentage==100:
        return  redirect('home')


    resp["activeCourseWork"] = resp["mineCourse"].current_course_work
    resp["courseWorkList"] = resp["course"].coursework_set.all()
    if resp["activeCourseWork"].work_type==CourseWork.LECTURE:
        return render(request, 'course/lecture.html', resp)
    else:
        return HandleQuiz(request, resp["activeCourseWork"])



def NextCourseWork(request, CourseId, CurrentCourseWorkId):
    course = Course.objects.get(pk=CourseId)
    mineCourse = MyCourse.objects.filter(course__course_id=course.course_id, user=request.user)
    if mineCourse.count() == 0:
        mineCourse = MyCourse(user=request.user, course=course)
        mineCourse.save()
    else:
        mineCourse = mineCourse.first()

    courseWorkList = course.coursework_set.all()

    nextCourseWorks = []
    for courseWork in courseWorkList:
        if(courseWork.pk  > CurrentCourseWorkId):
            nextCourseWorks.append(courseWork)
    if nextCourseWorks.__len__() == 0:
        mineCourse.percentage = 100
        mineCourse.course_completed = True
    else:
        mineCourse.percentage = (1.00 - (nextCourseWorks.__len__() / courseWorkList.count()))*100
        nextCourseWork = nextCourseWorks[nextCourseWorks.__len__() - 1]
        mineCourse.current_course_work = nextCourseWork

    mineCourse.save()

    if mineCourse.percentage==100:
        return  redirect('home')

    activeCourseWork = mineCourse.current_course_work
    # courseWorkList = course.coursework_set.all()
    nextURL = ''
    # if  is None:
    if activeCourseWork.work_type == CourseWork.LECTURE:
        return render(request, 'course/lecture.html', {
            'activeCourseWork': activeCourseWork,
            'course': course,
            'courseWorkList': courseWorkList,
            'nextURL': nextURL,
            'mineCourse': mineCourse,
        })
    else:
        return HandleQuiz(request, activeCourseWork)
    # return  HttpResponse('<h1>Pending work</h1>')


def HandleQuiz(request, activeCourseWork):
    # quizDetails = activeCourseWork.quiz_set

    mineQuiz = MyQuiz.objects.filter(course_work=activeCourseWork, user=request.user, is_finish=False).first()
    if mineQuiz is None:
        mineQuiz = MyQuiz()
        mineQuiz.course_work  = activeCourseWork
        mineQuiz.user = request.user
        mineQuiz.start_time = timezone.now()
        mineQuiz.is_finish = False
        mineQuiz.save()
    total_questions = json.loads(activeCourseWork.data)['total_questions']
    question_number = 1
    quizQuestion = Quiz.objects.filter(CourseWork=activeCourseWork, question_number=question_number).first()
    question = quizQuestion.quiz_question
    pk = quizQuestion.pk
    options = json.loads(quizQuestion.quiz_options)

    return render(request, 'course/quiz.html', {
        'mineQuiz':mineQuiz,
        'quizQuestion':quizQuestion,
        'question':question,
        'pk':pk,
        'myQuizPk':mineQuiz.pk,
        'activeCourseWork': activeCourseWork,
        'total_questions': total_questions,
        'question_number': question_number,
        'course': activeCourseWork.course,
        'options':options
    })


def SubmitQuizAnswer(request):
    mineQuiz = MyQuiz.objects.get(pk=request.POST.get('myQuizPk'))
    quizQuestion = Quiz.objects.get(pk=request.POST.get('pk'))
    activeCourseWork = quizQuestion.CourseWork
    total_questions = json.loads(activeCourseWork.data)['total_questions']
    quizDetail = MyQuizDetail()
    quizDetail.myQuiz = mineQuiz
    quizDetail.selected_option = request.POST.get('quizanswer')
    quizDetail.right_option = quizQuestion.right_option
    quizDetail.is_right = quizDetail.selected_option==quizDetail.right_option
    quizDetail.save()
    question_number = quizQuestion.question_number + 1
    if question_number>total_questions:
        return  QuizFinished(request, mineQuiz, activeCourseWork)
    quizQuestion = Quiz.objects.filter(CourseWork=activeCourseWork, question_number=question_number).first()
    question = quizQuestion.quiz_question
    pk = quizQuestion.pk
    options = json.loads(quizQuestion.quiz_options)
    return render(request, 'course/quiz.html', {
        'mineQuiz':mineQuiz,
        'quizQuestion':quizQuestion,
        'question':question,
        'pk':pk,
        'myQuizPk':mineQuiz.pk,
        'activeCourseWork': activeCourseWork,
        'total_questions': total_questions,
        'question_number': question_number,
        'course': activeCourseWork.course,
        'options':options})


def QuizFinished(request, myQuiz, activeCourseWork):
    UpdateQuizMarks(myQuiz)
    course = activeCourseWork.course
    mineCourse = MyCourse.objects.filter(course__course_id=course.course_id, user=request.user)
    if mineCourse.count() == 0:
        mineCourse = MyCourse(user=request.user, course=course)
        mineCourse.save()
    else:
        mineCourse = mineCourse.first()
    courseWorkList = course.coursework_set.all()

    nextCourseWorks = []
    for courseWork in courseWorkList:
        if (courseWork.pk > activeCourseWork.pk):
            nextCourseWorks.append(courseWork)
    if nextCourseWorks.__len__() == 0:
        mineCourse.percentage = 100
        mineCourse.course_completed = True
    else:
        mineCourse.percentage = (1.00 - (nextCourseWorks.__len__() / courseWorkList.count())) * 100
        nextCourseWork = nextCourseWorks[nextCourseWorks.__len__() - 1]
        mineCourse.current_course_work = nextCourseWork

    mineCourse.save()

    if mineCourse.percentage==100:
        return redirect('Index')

    activeCourseWork = mineCourse.current_course_work
    nextURL = ''
    # if  is None:
    if activeCourseWork.work_type == CourseWork.LECTURE:
        return render(request, 'course/lecture.html', {
            'activeCourseWork': activeCourseWork,
            'course': course,
            'courseWorkList': courseWorkList,
            'nextURL': nextURL,
            'mineCourse': mineCourse,
        })
    else:
        return HandleQuiz(request, activeCourseWork)


def UpdateQuizMarks(myQuiz):
    quizDetails = MyQuizDetail.objects.filter(myQuiz=myQuiz).all()
    totalMarks = 0
    for quizDetail in quizDetails:
        if quizDetail.is_right:
            totalMarks = totalMarks + 1

    myQuiz.obtained_marks = totalMarks
    myQuiz.total_marks = quizDetails.count()
    myQuiz.is_finish = True
    myQuiz.save()


