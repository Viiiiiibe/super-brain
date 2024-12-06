from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_our_team(self):
        response = self.client.get(reverse('about:our_team'))
        self.assertEqual(response.status_code, 200)

    def test_faq(self):
        response = self.client.get(reverse('about:faq'))
        self.assertEqual(response.status_code, 200)


class AboutTestsForContext(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = User.objects.create_user(
            username="Aaa",
            email="aaa@gmail.com",
            password="AaaBbbCcc123"
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username="Aaa", password="AaaBbbCcc123")

    def test_our_team(self):
        response = self.client.get(reverse('about:our_team'))
        self.assertEqual(response.status_code, 200)

    def test_faq(self):
        response = self.client.get(reverse('about:faq'))
        self.assertEqual(response.status_code, 200)
