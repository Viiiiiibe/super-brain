from django.contrib import admin
from .models import Category, Course, CourseProblem, PersonalCourse, PersonalProblem, Tournament, TournamentProblem

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseProblem)
admin.site.register(PersonalCourse)
admin.site.register(PersonalProblem)
admin.site.register(Tournament)
admin.site.register(TournamentProblem)
