from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class LogInTest(TestCase):

    def setUp(self):
        self.credentials = {
            'email': 'testuser@user.com',
            'first_name': 'Test',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post(
            '/accounts/login/',
            {'username': self.credentials['email'], 'password': self.credentials['password']},
            follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_edit_profile(self):

        self.test_login()

        new_name = "Badaboom"
        new_email = "boo@g.ru"

        response = self.client.post(
            '/edit_profile/', {'first_name': new_name, 'email': new_email}, follow=True)

        self.assertEqual(response.context['user'].first_name, new_name)
        self.assertEqual(response.context['user'].email, new_email)
