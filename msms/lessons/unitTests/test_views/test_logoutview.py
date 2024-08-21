from distutils.log import Log
from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.unitTests.helpers import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.create_user( 'janedog@example.org',
                first_name='Jane',
                last_name='Dog',
                password='Password123',
                is_active=True,
        )
    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')

    def test_get_log_out(self):
        self.client.login(username='janedog@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url=reverse('log_in')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')
        self.assertFalse(self._is_logged_in())