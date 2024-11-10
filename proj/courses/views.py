from django.shortcuts import render, get_object_or_404, redirect
from account.models import CustomUser
from courses.models import Category, Course, CourseProblem, PersonalCourse, PersonalProblem, Tournament, \
    TournamentProblem
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
    problem_obj = get_object_or_404(CourseProblem, pk=problem_id)
    problem_obj_course = problem_obj.course

    if (problem_obj_course.free or (
            not problem_obj_course.free and request.user.is_authenticated and request.user.end_of_subscription and
            request.user.end_of_subscription >= date.today())):
        notification = None
        try:
            next_problem = CourseProblem.objects.get(course=problem_obj_course,number=problem_obj.number+1)
            next_problem_id = next_problem.pk
        except:
            next_problem_id = None
        if request.method == 'POST':
            selected_answer = request.POST.get('answer')  # получаем ответ, выбранный пользователем
            if selected_answer:
                try:
                    selected_answer = int(selected_answer)  # проверяем, что ответ - это число
                    if selected_answer == problem_obj.right_answer:
                        if request.user.is_authenticated and problem_obj not in request.user.solved_problems.all():
                            # Если ответ правильный и задача решается парвый раз, начисляем пользователю очки
                            request.user.points += problem_obj.points
                            request.user.solved_problems.add(problem_obj)
                            request.user.save()
                        messages.success(request, 'Молодец! Ответ правильный. Приступим к следующему вопросу?')
                    else:
                        messages.error(request, 'Увы, но ответ неверный. Попробуешь еще раз ?')
                except ValueError:
                    messages.error(request, 'Увы, но ответ неверный. Попробуешь еще раз ?')
            else:
                messages.error(request, 'Ты не выбрал ответ. Попробуешь еще раз ?')
    else:
        notification = "Курс доступен по подписке"
        next_problem_id = None
    context = {
        'problem_obj': problem_obj,
        'next_problem_id': next_problem_id,
        'notification': notification,
    }
    return render(request, 'courses/problem.html', context)


def tournament(request):
    today = date.today()
    try:
        tournament_obj = Tournament.objects.get(end_date__gte=today,start_date__lte=today)
    except:
        tournament_obj = None
    tournament_top_users = CustomUser.objects.all().order_by('-tournament_points')[:10]
    if request.user.is_authenticated and tournament_obj and request.user in tournament_obj.participants.all():
        tournament_problems = TournamentProblem.objects.filter(tournament=tournament_obj).order_by('number')
        notification = None
    else:
        tournament_problems = None
        notification = "Участвуй и стань лучшим!"
    context = {
        'tournament_obj': tournament_obj,
        'tournament_top_users': tournament_top_users,
        'tournament_problems': tournament_problems,
        'notification': notification,
    }
    return render(request, 'courses/tournament.html', context)


@login_required
def tournament_problem(request, problem_id):
    today = date.today()
    user = request.user
    problem_obj = get_object_or_404(TournamentProblem, pk=problem_id)
    problem_obj_tournament = problem_obj.tournament

    if (problem_obj_tournament and
            problem_obj_tournament.end_date >= today >= problem_obj_tournament.start_date and
            user in problem_obj_tournament.participants.all()):
        try:
            next_problem = TournamentProblem.objects.get(course=problem_obj_tournament,number=problem_obj.number+1)
            next_problem_id = next_problem.pk
        except:
            next_problem_id = None

        if request.method == 'POST':
            selected_answer = request.POST.get('answer')  # получаем ответ, выбранный пользователем
            if selected_answer:
                try:
                    selected_answer = int(selected_answer)  # проверяем, что ответ - это число
                    if (selected_answer == problem_obj.right_answer and
                            problem_obj not in user.solved_tournament_problems.all()):
                        # Если ответ правильный и задача решается парвый раз,
                        # начисляем пользователю очки турнира и обычные + добавляем в решенные
                        request.user.tournament_points += problem_obj.points
                        request.user.points += problem_obj.points
                        request.user.solved_tournament_problems.add(problem_obj)
                        request.user.save()
                        messages.success(request, 'Ответ засчитан! Приступим к следующему вопросу?')
                    elif (selected_answer != problem_obj.right_answer and
                            problem_obj not in user.solved_tournament_problems.all()):
                        # Если ответ не правильный и задача решается парвый раз,
                        # добавляем в решенные
                        request.user.solved_tournament_problems.add(problem_obj)
                        request.user.save()
                        messages.success(request, 'Ответ засчитан! Приступим к следующему вопросу?')
                    else:
                        messages.error(request, 'Эй! Ты уже отвечал! Так не считается!😝')
                except ValueError:
                    messages.error(request, 'Не могу прочитать ответ... Попробуешь еще раз ?')
            else:
                messages.error(request, 'Ты не выбрал ответ. Попробуешь еще раз ?')
    else:
        return redirect('tournament', )

    context = {
        'problem_obj': problem_obj,
        'next_problem_id': next_problem_id,
    }
    return render(request, 'courses/tournament_problem.html', context)


@login_required
def current_courses(request):
    current_courses_list = []

    # Проверка на авторизацию пользователя
    if request.user.is_authenticated:
        user = request.user

        # Получаем все экземпляры PersonalCourse, где первая задача решена, а последняя нет
        all_personal_course_obj = PersonalCourse.objects.all().order_by('title')
        for personal_course_obj in all_personal_course_obj:
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
            first_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').first()
            last_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').last()
            if first_problem and last_problem:
                if (
                        first_problem in user.solved_problems.all()
                        and last_problem not in user.solved_problems.all()
                ):
                    current_courses_list.append(course_obj)

    # Передаем объединенный список в контекст
    context = {
        'current_courses_list': current_courses_list
    }

    return render(request, 'courses/current_courses.html', context)


@login_required
def completed_courses(request):
    completed_courses_list = []

    # Проверка на авторизацию пользователя
    if request.user.is_authenticated:
        user = request.user

        # Получаем все экземпляры PersonalCourse, где последняя задача решена
        all_personal_course_obj = PersonalCourse.objects.all().order_by('title')
        for personal_course_obj in all_personal_course_obj:
            last_problem = PersonalProblem.objects.filter(course=personal_course_obj).order_by('number').last()
            if last_problem:
                if last_problem in user.solved_personal_problems.all():
                    completed_courses_list.append(personal_course_obj)

        # Получаем все экземпляры Course, где первая задача решена, а последняя нет
        all_course_obj = Course.objects.all().order_by('title')
        for course_obj in all_course_obj:
            last_problem = CourseProblem.objects.filter(course=course_obj).order_by('number').last()
            if last_problem:
                if last_problem in user.solved_problems.all():
                    completed_courses_list.append(course_obj)

    # Передаем объединенный список в контекст
    context = {
        'completed_courses_list': completed_courses_list
    }
    return render(request, 'courses/completed_courses.html', context)


@login_required
def personal_courses(request):
    user = request.user
    courses = PersonalCourse.objects.filter(user=user).order_by('title')
    context = {
        'courses': courses,
    }
    return render(request, 'courses/personal_courses.html', context)


@login_required
def personal_course(request, slug):
    user = request.user
    course_obj = get_object_or_404(PersonalCourse, slug=slug)
    if user != course_obj.user:
        return redirect('personal_courses', )
    else:
        problems = PersonalProblem.objects.filter(course=course_obj).order_by('number')
    context = {
        'course': course_obj,
        'problems': problems,
    }
    return render(request, 'courses/personal_course.html', context)


@login_required
def personal_problem(request, problem_id):
    user = request.user
    problem_obj = get_object_or_404(PersonalProblem, pk=problem_id)
    problem_obj_course = problem_obj.course
    if user != problem_obj_course.user:
        return redirect('personal_courses', )
    else:
        try:
            next_problem = PersonalProblem.objects.get(course=problem_obj_course,number=problem_obj.number+1)
            next_problem_id = next_problem.pk
        except:
            next_problem_id = None
        if request.method == 'POST':
            selected_answer = request.POST.get('answer')  # получаем ответ, выбранный пользователем
            if selected_answer:
                try:
                    selected_answer = int(selected_answer)  # проверяем, что ответ - это число
                    if selected_answer == problem_obj.right_answer:
                        if problem_obj not in request.user.solved_personal_problems.all():
                            # Если ответ правильный и задача решается парвый раз, начисляем пользователю очки
                            request.user.points += problem_obj.points
                            request.user.solved_personal_problems.add(problem_obj)
                            request.user.save()
                        messages.success(request, 'Молодец! Ответ правильный. Приступим к следующему вопросу?')
                    else:
                        messages.error(request, 'Увы, но ответ неверный. Попробуешь еще раз ?')
                except ValueError:
                    messages.error(request, 'Увы, но ответ неверный. Попробуешь еще раз ?')
            else:
                messages.error(request, 'Ты не выбрал ответ. Попробуешь еще раз ?')
    context = {
        'problem_obj': problem_obj,
        'next_problem_id': next_problem_id,
    }
    return render(request, 'courses/personal_problem.html', context)
