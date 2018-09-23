from django.db import models

# Create your models here.

class Course(models.Model):

    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    course_credit_hours = models.IntegerField()
    cover_photo = models.CharField(max_length=300, default=' ')
    def __str__(self):
        return self.course_name


class CourseWork(models.Model):
    LECTURE = 1
    QUIZ = 2
    TypeChoices = (
        (LECTURE, 'Lecture'),
        (QUIZ, 'Quiz'),
    )

    work_name = models.CharField(max_length=50)
    work_type = models.PositiveSmallIntegerField(choices=TypeChoices, null=True, blank=True)
    lecture_url = models.CharField(max_length=500, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    next_course_work = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.work_name + " - "+self.course.course_name

class Quiz(models.Model):
    RADIO = 1
    SELECT = 2
    TypeChoices = (
        (RADIO , 'One Option'),
        (SELECT, 'Multiple Select'),
    )

    quiz_type = models.PositiveSmallIntegerField(choices=TypeChoices, null=True, blank=True)
    quiz_question = models.CharField(max_length=500)
    quiz_options = models.TextField(null=True, blank=True)
    right_option = models.CharField(max_length=5, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    CourseWork  = models.ForeignKey(CourseWork, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    def __str__(self):
        return self.quiz_question





