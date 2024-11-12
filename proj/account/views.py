from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from account.models import CustomUser
from blog.models import News
from courses.models import PersonalCourse, PersonalProblem, Course, CourseProblem
from django.db.models import Window, F
from django.db.models.functions import Rank


def signup(request):
    return render(request, 'account/signup.html')


def logout(request):
    return render(request, 'account/logout.html')


def login(request):
    return render(request, 'account/login.html')


def password_change(request):
    return render(request, 'account/password_change_form.html')


def password_change_done(request):
    return render(request, 'account/password_change_done.html')


def password_reset(request):
    return render(request, 'account/password_reset_form.html')


def password_reset_done(request):
    return render(request, 'account/password_reset_done.html')


def password_reset_confirm(request):
    return render(request, 'account/password_reset_confirm.html')


def password_reset_complete(request):
    return render(request, 'account/password_reset_complete.html')


@login_required
def personal_account_main(request):
    user = request.user
    # Место в рейтинге
    top_users = CustomUser.objects.annotate(
        rank=Window(
            expression=Rank(),
            order_by=F('points').desc()
        )
    ).order_by('-points')

    # Ищем позицию авторизованного пользователя
    user_position_in_top = top_users.get(id=request.user.id).rank

    # Личные курсы
    personal_courses_list = PersonalCourse.objects.filter(user=user).order_by('title')[:3]

    # Текущие курсы
    current_courses_list = []
    # Получаем все экземпляры PersonalCourse, где первая задача решена, а последняя нет
    all_personal_course_obj = PersonalCourse.objects.all().order_by('title')
    for personal_course_obj in all_personal_course_obj:
        if len(current_courses_list) == 3:
            break
        first_problem = PersonalProblem.objects.filter(course=personal_course_obj).order_by('number').first()
        last_problem = PersonalProblem.objects.filter(course=personal_course_obj).order_by('number').last()
        if first_problem and last_problem:
            if (
                    first_problem in user.solved_personal_problems.all()
                    and last_problem not in user.solved_personal_problems.all()
            ):
                current_courses_list.append(personal_course_obj)

    # Получаем все экземпляры Course, где первая задача решена, а последняя нет
    all_course_obj = Course.objects.all().order_by('title')
    for course_obj in all_course_obj:
        if len(current_courses_list) == 3:
            break
        first_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').first()
        last_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').last()
        if first_problem and last_problem:
            if (
                    first_problem in user.solved_problems.all()
                    and last_problem not in user.solved_problems.all()
            ):
                current_courses_list.append(course_obj)

    # Пройденые курсы
    completed_courses_list = []
    # Получаем все экземпляры PersonalCourse, где последняя задача решена
    all_personal_course_obj = PersonalCourse.objects.all().order_by('title')
    for personal_course_obj in all_personal_course_obj:
        if len(completed_courses_list) == 3:
            break
        last_problem = PersonalProblem.objects.filter(course=personal_course_obj).order_by('number').last()
        if last_problem:
            if last_problem in user.solved_personal_problems.all():
                completed_courses_list.append(personal_course_obj)

    # Получаем все экземпляры Course, где первая задача решена, а последняя нет
    all_course_obj = Course.objects.all().order_by('title')
    for course_obj in all_course_obj:
        if len(completed_courses_list) == 3:
            break
        last_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').last()
        if last_problem:
            if last_problem in user.solved_problems.all():
                completed_courses_list.append(course_obj)

    # Новости
    news_list = News.objects.all().order_by('-pub_date')[:3]
    context = {
        'news_list': news_list,
        'user_position_in_top': user_position_in_top,
        'personal_courses_list': personal_courses_list,
        'completed_courses_list': completed_courses_list,
        'current_courses_list': current_courses_list,
    }

    return render(request, 'account/personal_account_main.html', context)


def order_an_individual_course(request):
    return render(request, 'account/order_an_individual_course.html')


def order_an_individual_course_done(request):
    return render(request, 'account/order_an_individual_course_done.html')


def rating(request):
    all_top_users = CustomUser.objects.annotate(
        rank=Window(
            expression=Rank(),
            order_by=F('points').desc()
        )
    ).order_by('-points')
    top_users = all_top_users[:10]
    if request.user.is_authenticated:
        # Ищем позицию авторизованного пользователя
        user_position_in_top = all_top_users.get(id=request.user.id).rank
    else:
        user_position_in_top = None

    context = {
        'top_users': top_users,
        'user_position_in_top': user_position_in_top,
    }
    return render(request, 'account/rating.html', context)
