from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Category, Course, CourseProblem, PersonalCourse, PersonalProblem, Tournament, TournamentProblem
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()


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

    def setUp(self):
        self.client = Client()
        self.client.login(username="Aaa", password="AaaBbbCcc123")

    def test_all_courses_show_correct_context(self):
        response = self.client.get(reverse('all_courses'))

        categories_with_courses = response.context['categories_with_courses'][0]['category'].slug
        self.assertEqual(categories_with_courses, 'category1')

        current_courses = response.context['current_courses'][0].slug
        self.assertEqual(current_courses, 'course1')

        current_date = response.context['current_date']
        self.assertEqual(current_date, now().date())

    def test_category_courses_show_correct_context(self):
        response = self.client.get(reverse('category_courses', kwargs={'slug': "category1"}))

        category = response.context['category'].slug
        self.assertEqual(category, 'category1')

        courses = response.context['courses'][0].slug
        self.assertEqual(courses, 'course1')

    def test_course_show_correct_context(self):
        response = self.client.get(reverse('course', kwargs={'slug': "course1"}))

        course = response.context['course'].slug
        self.assertEqual(course, 'course1')

        problems_dict = dict()
        problems_dict['problem1'] = response.context['problems'][0].pk
        problems_dict['problem2'] = response.context['problems'][1].pk
        self.assertEqual(problems_dict['problem1'], 1)
        self.assertEqual(problems_dict['problem2'], 2)
        notification = response.context['notification']
        self.assertEqual(notification, None)

    def test_problem_show_correct_context(self):
        response = self.client.get(reverse('problem', kwargs={'problem_id': "1"}))

        problem_obj = response.context['problem_obj'].pk
        self.assertEqual(problem_obj, 1)

        next_problem_id = response.context['next_problem_id']
        self.assertEqual(next_problem_id, 2)

        notification = response.context['notification']
        self.assertEqual(notification, None)

    def test_tournament_show_correct_context(self):
        response = self.client.get(reverse('tournament'))

        notification = response.context['notification']
        self.assertEqual(notification, None)

        tournament_obj = response.context['tournament_obj'].pk
        self.assertEqual(tournament_obj, 1)

        tournament_top_users = response.context['tournament_top_users'][0].username
        self.assertEqual(tournament_top_users, "Aaa")

        tournament_problems = response.context['tournament_problems'][0].pk
        self.assertEqual(tournament_problems, 1)

        user_position_in_tournament_top = response.context['user_position_in_tournament_top']
        self.assertEqual(user_position_in_tournament_top, 1)

    def test_tournament_problem_show_correct_context(self):
        response = self.client.get(reverse('tournament_problem', kwargs={'problem_id': "1"}))

        problem_obj = response.context['problem_obj'].pk
        self.assertEqual(problem_obj, 1)

        next_problem_id = response.context['next_problem_id']
        self.assertEqual(next_problem_id, None)

    def test_current_courses_show_correct_context(self):
        response = self.client.get(reverse('current_courses'))

        current_courses_list = response.context['current_courses_list'][0].slug
        self.assertEqual(current_courses_list, 'course1')

    def test_completed_courses_show_correct_context(self):
        response = self.client.get(reverse('completed_courses'))

        completed_courses_list = response.context['completed_courses_list'][0].slug
        self.assertEqual(completed_courses_list, 'personal_course1')

    def test_personal_courses_show_correct_context(self):
        response = self.client.get(reverse('personal_courses'))

        courses = response.context['courses'][0].slug
        self.assertEqual(courses, 'personal_course1')

    def test_personal_course_correct_context(self):
        response = self.client.get(reverse('personal_course', kwargs={'slug': "personal_course1"}))

        course = response.context['course'].slug
        self.assertEqual(course, 'personal_course1')

        problems_dict = dict()
        problems_dict['problem1'] = response.context['problems'][0].pk
        self.assertEqual(problems_dict['problem1'], 1)

    def test_personal_problem_show_correct_context(self):
        response = self.client.get(reverse('personal_problem', kwargs={'problem_id': "1"}))

        problem_obj = response.context['problem_obj'].pk
        self.assertEqual(problem_obj, 1)

        next_problem_id = response.context['next_problem_id']
        self.assertEqual(next_problem_id, None)
