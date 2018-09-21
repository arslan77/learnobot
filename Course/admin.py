from django.contrib import admin
from Course.models import Course, CourseWork, Quiz

# Register your models here.

# admin.site.(Course)
admin.site.register(Course)
admin.site.register(CourseWork)
admin.site.register(Quiz)
