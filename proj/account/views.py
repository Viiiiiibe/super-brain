from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import CustomUser
from blog.models import News
from courses.models import PersonalCourse, PersonalProblem, Course, CourseProblem
from django.db.models import Window, F
from django.db.models.functions import Rank
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView)
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from proj.settings import MANAGER_EMAIL
from account.tasks import send_order_email


class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('index')
    template_name = 'account/signup.html'


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'


class UserPasswordChange(PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")
    template_name = "account/password_change_form.html"


class UserPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("account:password_reset_done")
    template_name = "account/password_reset_form.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")
    template_name = "account/password_reset_confirm.html"


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


@login_required
def order(request):
    if request.method == "POST":
        # Считываем данные из формы
        contact_method = request.POST.get('contact_method')
        contact_data = request.POST.get('contact_data')
        service = request.POST.get('service')

        # Проверяем, чтобы обязательные поля были заполнены
        if contact_method is None or contact_data is None or service is None:
            messages.error(request, "Пожалуйста, заполните все поля формы.")
            return redirect('account:order')  # Перенаправление на ту же страницу

        user = request.user
        # Формируем текст сообщения
        subject = f"Новый заказ на {service}"
        message = (
            f"Пользователь: {user.pk} - {user.username} - {user.email}\n"
            f"Тип связи: {contact_method}\n"
            f"Контакт: {contact_data}\n"
            f"Услуга: {service}"
        )
        manager_email = MANAGER_EMAIL

        try:
            # Отправляем письмо через задачу Celery
            send_order_email.delay(subject, message, [manager_email])
            # Перенаправляем пользователя на страницу подтверждения
            return redirect('account:order_done')
        except Exception:
            messages.error(request, f"Произошла ошибка при отправке письма попробуйте позже")
            return redirect('account:order')

    return render(request, 'account/order.html', )


def order_done(request):
    return render(request, 'account/order_done.html')


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
