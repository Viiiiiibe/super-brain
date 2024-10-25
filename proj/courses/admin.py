from django.contrib import admin
from .models import Category, Course, Problem, PersonalCourse, PersonalProblem, Tournament, TournamentProblem

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Problem)
admin.site.register(PersonalCourse)
admin.site.register(PersonalProblem)
admin.site.register(Tournament)
admin.site.register(TournamentProblem)
