from django.shortcuts import render


def index(request):
    return render(request, 'courses/index.html')


def all_courses(request):
    return render(request, 'courses/all_courses.html')


def category_courses(request, slug):
    return render(request, 'courses/category_courses.html')


def course(request, slug):
    return render(request, 'courses/course.html')


def problem(request, problem_id):
    return render(request, 'courses/problem.html')


def tournament(request, tournament_id):
    return render(request, 'courses/tournament.html')


def tournament_problem(request, tournament_problem_id):
    return render(request, 'courses/tournament_problem.html')
