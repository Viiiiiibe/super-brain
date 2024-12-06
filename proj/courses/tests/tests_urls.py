from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Category, Course, CourseProblem, PersonalCourse, PersonalProblem, Tournament, TournamentProblem
from proj.settings import AUTH_USER_MODEL
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()


class CoursesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        i = 1
        category = Category.objects.create(
            pk=i,
            title=f'Категория номер {i}',
            slug=f'category{i}',
        )

        user = User.objects.create_user(
            username=f'testuser{i}',
            email=f'password{i}'
        )

        course = Course.objects.create(
            pk=i,
            title=f'Курс номер {i}',
            slug=f'course{i}',
            category=category
        )

        CourseProblem.objects.create(
            course=course,
            number=i,
            right_answer=i,
        )

        PersonalCourse.objects.create(
            pk=i,
            title=f'Курс номер {i}',
            slug=f'course{i}',
            user=user
        )

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_all_courses(self):
        response = self.guest_client.get(reverse('all_courses'))
        self.assertEqual(response.status_code, 200)

    def test_category_courses(self):
        # Пример с валидным slug
        response = self.guest_client.get(reverse('category_courses', kwargs={'slug': 'category1'}))
        self.assertEqual(response.status_code, 200)

    def test_course(self):
        # Пример с валидным slug
        response = self.guest_client.get(reverse('course', kwargs={'slug': 'course1'}))
        self.assertEqual(response.status_code, 200)

    def test_problem(self):
        # Пример с валидным problem_id
        response = self.guest_client.get(reverse('problem', kwargs={'problem_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_tournament(self):
        response = self.guest_client.get(reverse('tournament'))
        self.assertEqual(response.status_code, 200)

    def test_tournament_problem(self):
        # Пример с валидным problem_id
        response = self.guest_client.get(reverse('tournament_problem', kwargs={'problem_id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_current_courses(self):
        response = self.guest_client.get(reverse('current_courses'))
        self.assertEqual(response.status_code, 302)

    def test_completed_courses(self):
        response = self.guest_client.get(reverse('completed_courses'))
        self.assertEqual(response.status_code, 302)

    def test_personal_courses(self):
        response = self.guest_client.get(reverse('personal_courses'))
        self.assertEqual(response.status_code, 302)

    def test_personal_course(self):
        # Пример с валидным slug
        response = self.guest_client.get(reverse('personal_course', kwargs={'slug': 'course1'}))
        self.assertEqual(response.status_code, 302)

    def test_personal_problem(self):
        # Пример с валидным problem_id
        response = self.guest_client.get(reverse('personal_problem', kwargs={'problem_id': 1}))
        self.assertEqual(response.status_code, 302)


class CoursesTestsForContext(TestCase):
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
        course1 = Course.objects.create(
            pk=1,
            title='Курс номер 1',
            slug='course1',
            category=Category.objects.get(pk=1),
        )
        course1_problem1 = CourseProblem.objects.create(
            pk=1,
            number=1,
            text='1',
            right_answer=1,
            course=Course.objects.get(pk=1),
        )
        course1_problem2 = CourseProblem.objects.create(
            pk=2,
            number=2,
            text='2',
            right_answer=2,
            course=Course.objects.get(pk=1),
        )

        personal_course = PersonalCourse.objects.create(
            pk=1,
            title='Личный курс номер 1',
            slug='personal_course1',
            user=User.objects.get(username="Aaa")
        )
        personal_problem = PersonalProblem.objects.create(
            pk=1,
            number=1,
            text='1',
            right_answer=1,
            course=PersonalCourse.objects.get(pk=1),
        )

        tournament = Tournament.objects.create(
            pk=1,
            title='Турнир номер 1',
            start_date=now().date(),
            end_date=now().date() + timedelta(days=30),
        )
        tournament.participants.set(User.objects.filter(username="Aaa"))
        tournament_problem = TournamentProblem.objects.create(
            pk=1,
            number=1,
            text='1',
            right_answer=1,
            tournament=Tournament.objects.get(pk=1),
        )

        user.solved_problems.set(CourseProblem.objects.filter(pk=1))
        user.solved_personal_problems.set(PersonalProblem.objects.filter(pk=1))

    def setUp(self):
        self.client = Client()
        self.client.login(username="Aaa", password="AaaBbbCcc123")

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_all_courses(self):
        response = self.client.get(reverse('all_courses'))
        self.assertEqual(response.status_code, 200)

    def test_category_courses(self):
        # Пример с валидным slug
        response = self.client.get(reverse('category_courses', kwargs={'slug': 'category1'}))
        self.assertEqual(response.status_code, 200)

    def test_course(self):
        # Пример с валидным slug
        response = self.client.get(reverse('course', kwargs={'slug': 'course1'}))
        self.assertEqual(response.status_code, 200)

    def test_problem(self):
        # Пример с валидным problem_id
        response = self.client.get(reverse('problem', kwargs={'problem_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_tournament(self):
        response = self.client.get(reverse('tournament'))
        self.assertEqual(response.status_code, 200)

    def test_tournament_problem(self):
        # Пример с валидным problem_id
        response = self.client.get(reverse('tournament_problem', kwargs={'problem_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_current_courses(self):
        response = self.client.get(reverse('current_courses'))
        self.assertEqual(response.status_code, 200)

    def test_completed_courses(self):
        response = self.client.get(reverse('completed_courses'))
        self.assertEqual(response.status_code, 200)

    def test_personal_courses(self):
        response = self.client.get(reverse('personal_courses'))
        self.assertEqual(response.status_code, 200)

    def test_personal_course(self):
        # Пример с валидным slug
        response = self.client.get(reverse('personal_course', kwargs={'slug': 'personal_course1'}))
        self.assertEqual(response.status_code, 200)

    def test_personal_problem(self):
        # Пример с валидным problem_id
        response = self.client.get(reverse('personal_problem', kwargs={'problem_id': 1}))
        self.assertEqual(response.status_code, 200)
