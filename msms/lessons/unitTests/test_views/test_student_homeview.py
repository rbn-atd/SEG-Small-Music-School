from django.test import TestCase
from django.urls import reverse
from lessons.unitTests.helpers import reverse_with_next

"""Unit tests for accept_request view"""
class StudentHomeViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('student_home')

    # def test_student_home_redirects_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('log_in', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)