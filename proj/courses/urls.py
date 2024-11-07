from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('all_courses/<slug:slug>/', views.category_courses, name='category_courses'),
    path('course/<slug:slug>/', views.course, name='course'),
    path('problem/<int:problem_id>/', views.problem, name='problem'),
    path('tournament/', views.tournament, name='tournament'),
    path('tournament_problem/<int:tournament_problem_id>/', views.tournament_problem, name='tournament_problem'),
    path('current_courses/', views.current_courses, name='current_courses'),
    path('completed_courses/', views.completed_courses, name='completed_courses'),
    path('personal_courses/', views.personal_courses, name='personal_courses'),
    path('personal_course/<slug:slug>/', views.personal_course, name='personal_course'),
    path('personal_problem/<int:problem_id>/', views.personal_problem, name='personal_problem'),
]
