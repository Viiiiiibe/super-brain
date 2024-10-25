from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from courses.models import CourseProblem, PersonalProblem, TournamentProblem


class CustomUser(AbstractUser):
    patronymic = models.CharField(blank=True, null=True, max_length=150, verbose_name='Отчество')
    email = models.EmailField(_('email address'), unique=True)
    end_of_subscription = models.DateField(
        verbose_name='Дата завершения подписки', blank=True, null=True, auto_now_add=False)
    points = models.IntegerField('Очки опыта', blank=True, null=True, default=0)
    tournament_points = models.IntegerField(
        'Очки опыта за текущий турнир', blank=True, null=True, default=0)
    solved_problems = models.ManyToManyField(
        CourseProblem,
        related_name='users_who_have_solved',
        verbose_name='Решенные задачи'
    )
    solved_personal_problems = models.ManyToManyField(
        PersonalProblem,
        related_name='users_who_have_solved',
        verbose_name='Решенные задачи личных курсов'
    )
    solved_tournament_problems = models.ManyToManyField(
        TournamentProblem,
        related_name='users_who_have_solved',
        verbose_name='Решенные задачи турнира'
    )
