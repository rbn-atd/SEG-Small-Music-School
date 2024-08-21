from django.test import TestCase
from django.urls import reverse
from lessons.forms import TermForm
from lessons.models import Term
from lessons.unitTests.helpers import reverse_with_next

"""Unit tests for create_term view"""
class CreateTermViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('create_term')

    # def test_create_term_view_redirects_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)