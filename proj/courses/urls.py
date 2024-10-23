from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('all_courses/<slug:slug>/', views.category_courses, name='category_courses'),
    path('course/<slug:slug>/', views.course, name='course'),
    path('problem/<int:problem_id>/', views.problem, name='problem'),
    path('tournament/<int:tournament_id>/', views.tournament, name='tournament'),
    path('tournament_problem/<int:tournament_problem_id>/', views.tournament_problem, name='tournament_problem'),
]
