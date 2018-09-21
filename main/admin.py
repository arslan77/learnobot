from django.contrib import admin

# Register your models here.
from main.models import MyCourse, MyQuiz, MyQuizDetail

admin.site.register(MyCourse)
admin.site.register(MyQuiz)
admin.site.register(MyQuizDetail)
