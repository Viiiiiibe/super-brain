from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class AccountURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_signup(self):
        response = self.client.get(reverse('account:signup'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_password_change(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)

    def test_password_change_done(self):
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 302)

    def test_password_reset(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm(self):
        uidb64 = 'valid_uid'
        token = 'valid_token'
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_personal_account_main(self):
        response = self.client.get(reverse('account:personal_account_main'))
        self.assertEqual(response.status_code, 302)

    def test_order(self):
        response = self.client.get(reverse('account:order'))
        self.assertEqual(response.status_code, 302)

    def test_rating(self):
        response = self.client.get(reverse('account:rating'))
        self.assertEqual(response.status_code, 200)


class AccountTestsForContext(TestCase):
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

    def test_signup(self):
        response = self.client.get(reverse('account:signup'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_password_change(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_done(self):
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm(self):
        uidb64 = 'valid_uid'
        token = 'valid_token'
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_personal_account_main(self):
        response = self.client.get(reverse('account:personal_account_main'))
        self.assertEqual(response.status_code, 200)

    def test_order(self):
        response = self.client.get(reverse('account:order'))
        self.assertEqual(response.status_code, 200)

    def test_rating(self):
        response = self.client.get(reverse('account:rating'))
        self.assertEqual(response.status_code, 200)
