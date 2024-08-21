from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.forms import LogInForm
from lessons.unitTests.helpers import LogInTester, reverse_with_next

"""Unit tests for log in view"""
class LogInViewTestCase(TestCase, LogInTester):
    def setUp(self):
        self.url = reverse('log_in')
        self.user=User.objects.create_user(
            'janedog@example.org',
            first_name='Jane',
            last_name='Dog',
            password='Password123'
        )

    def test_login_url(self):
        self.assertEqual(self.url, '/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        # next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        # self.assertFalse(next)

    # def test_get_log_in_with_redirect(self):
    #     destination_url = reverse('student_home')
    #     self.url=reverse_with_next('log_in', destination_url)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'log_in.html')
    #     form = response.context['form']
    #     # next = response.context['next']
    #     self.assertTrue(isinstance(form, LogInForm))
    #     self.assertFalse(form.is_bound)
    #     # self.assertEqual(next, destination_url)

    def test_unsuccessful_login(self):
        form_input = { 'username': 'janedog@example.org', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_login(self):
        form_input = { 'username': 'janedog@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input,follow=True)
        self.assertTrue(self._is_logged_in())
        response_url=reverse('student_home')#replace with student homepage view
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_home.html')#same thing here

    def test_successful_login_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = { 'username': 'janedog@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input,follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
