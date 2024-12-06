from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from courses.models import Category, Course, CourseProblem, PersonalCourse, PersonalProblem, Tournament, \
    TournamentProblem
from django.utils.timezone import now
from datetime import timedelta
from blog.models import News

User = get_user_model()


class AccountTestsForContext(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(
            username="Aaa",
            email="aaa@gmail.com",
            password="AaaBbbCcc123"
        )

        Category.objects.create(
            pk=1,
            title='Категория номер 1',
            slug='category1',
        )
        Course.objects.create(
            pk=1,
            title='Курс номер 1',
            slug='course1',
            category=Category.objects.get(pk=1),
            free=True,
        )
        CourseProblem.objects.create(
            pk=1,
            number=1,
            text='1',
            right_answer=1,
            course=Course.objects.get(pk=1),
        )
        CourseProblem.objects.create(
            pk=2,
            number=2,
            text='2',
            right_answer=2,
            course=Course.objects.get(pk=1),
        )

        PersonalCourse.objects.create(
            pk=1,
            title='Личный курс номер 1',
            slug='personal_course1',
            user=User.objects.get(username="Aaa")
        )
        PersonalProblem.objects.create(
            pk=1,
            number=1,
            text='1',
            right_answer=1,
            course=PersonalCourse.objects.get(pk=1),
        )

        tournament = Tournament.objects.create(
            pk=1,
            title='Турнир номер 1',
            start_date=now().date() - timedelta(days=1),
            end_date=now().date() + timedelta(days=30),
        )
        tournament.participants.set(User.objects.filter(username="Aaa"))
        TournamentProblem.objects.create(
            pk=1,
            number=1,
            text='1',
            right_answer=1,
            tournament=Tournament.objects.get(pk=1),
        )

        user.solved_problems.set(CourseProblem.objects.filter(pk=1))
        user.solved_personal_problems.set(PersonalProblem.objects.filter(pk=1))

        News.objects.create(
            pk=1,
            title='Заголовок',
            text='Текст',
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username="Aaa", password="AaaBbbCcc123")

    def test_personal_account_main_show_correct_context(self):
        response = self.client.get(reverse('account:personal_account_main'))

        news_list = response.context['news_list'][0].pk
        self.assertEqual(news_list, 1)

        user_position_in_top = response.context['user_position_in_top']
        self.assertEqual(user_position_in_top, 1)

        personal_courses_list = response.context['personal_courses_list'][0].slug
        self.assertEqual(personal_courses_list, 'personal_course1')

        current_courses_list = response.context['current_courses_list'][0].slug
        self.assertEqual(current_courses_list, 'course1')

        completed_courses_list = response.context['completed_courses_list'][0].slug
        self.assertEqual(completed_courses_list, 'personal_course1')

    def test_rating_show_correct_context(self):
        response = self.client.get(reverse('account:rating'))

        top_users = response.context['top_users'][0].pk
        self.assertEqual(top_users, 1)

        user_position_in_top = response.context['user_position_in_top']
        self.assertEqual(user_position_in_top, 1)
