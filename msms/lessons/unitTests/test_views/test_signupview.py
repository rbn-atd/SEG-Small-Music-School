from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from lessons.forms import SignUpForm
from lessons.models import User
from lessons.unitTests.helpers import LogInTester

"""Unit tests for sign up view"""
class SignUpViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('sign_up')

        self.form_input={
                'first_name': 'Jane',
                'last_name': 'Dog',
                'username': 'janedog@example.org',
                'new_password': 'Password123',
                'password_confirmation': 'Password123'

            }

    def test_sign_up_url(self):
        self.assertEqual(reverse('sign_up'), '/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):
        self.form_input['username']='No'
        before_count=User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count=User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count=User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count=User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url=reverse('student_home')#replace with student homepage view
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_home.html')#same thing here
        user = User.objects.get(username='janedog@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Dog')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
