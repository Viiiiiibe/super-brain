from django.shortcuts import render, get_object_or_404

from courses.models import Category, Course, CourseProblem, PersonalCourse
from datetime import date
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'courses/index.html')


def all_courses(request):
    categories = Category.objects.all()
    categories_with_courses = []

    # Формируем список категорий с 4 курсами для каждой категории
    for category in categories:
        courses = Course.objects.filter(category=category).order_by('title')[:4]
        categories_with_courses.append({
            'category': category,
            'courses': courses
        })

        # Получаем 3 курса, где первая задача решена, а последняя нет
        current_courses_list = []

        # Проверка на авторизацию пользователя
        if request.user.is_authenticated:
            user = request.user

            all_course_obj = Course.objects.all().order_by('title')

            for course_obj in all_course_obj:
                # Определяем первую и последнюю задачу по номеру в курсе
                first_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').first()
                last_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').last()

                # Проверяем условия: первая решена, а последняя - нет
                if first_problem and last_problem:
                    if (
                            first_problem in user.solved_problems.all()
                            and last_problem not in user.solved_problems.all()
                    ):
                        current_courses_list.append(course_obj)
                        if len(current_courses_list) == 3:
                            break

    context = {
        'categories_with_courses': categories_with_courses,
        'current_courses': current_courses_list,
    }
    return render(request, 'courses/all_courses.html', context)


def category_courses(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(category=category).order_by('title')
    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'courses/category_courses.html', context)


def course(request, slug):
    course_obj = get_object_or_404(Course, slug=slug)
    if not course_obj.free:
        if (request.user.is_authenticated and request.user.end_of_subscription and
                request.user.end_of_subscription >= date.today()):
            problems = CourseProblem.objects.filter(course=course_obj).order_by('number')
            notification = None
        else:
            problems = None
            notification = "Курс доступен по подписке"
    else:
        problems = CourseProblem.objects.filter(course=course_obj).order_by('number')
        notification = None
    context = {
        'course': course_obj,
        'problems': problems,
        'notification': notification,
    }
    return render(request, 'courses/course.html', context)


def problem(request, problem_id):
    return render(request, 'courses/problem.html')


def tournament(request, tournament_id):
    return render(request, 'courses/tournament.html')


def tournament_problem(request, tournament_problem_id):
    return render(request, 'courses/tournament_problem.html')


def current_courses(request):
    return render(request, 'courses/current_courses.html')


def completed_courses(request):
    return render(request, 'courses/completed_courses.html')


@login_required
def personal_courses(request):
    user = request.user
    courses = PersonalCourse.objects.filter(user=user).order_by('title')
    context = {
        'courses': courses,
    }
    return render(request, 'courses/personal_courses.html', context)
