from django.core.exceptions import ValidationError
from django.test import TestCase
from django import forms
from lessons.forms import ContactForm
from lessons.models import Request
from lessons.models import User

"""Unit tests for the student request form"""

class RequestFormTestCase(TestCase):
    def setUp(self):    
        self.form_input={
            'availability': ['Monday'],
            'number_Of_Lessons': '1',
            'length': '30 mins',
            'interval': 'every week',
            'body': 'Test message'
        }
                
    def test_valid_sign_up_form(self):
        form = ContactForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_all_fields(self):
        form = ContactForm()
        self.assertIn('availability', form.fields)
        self.assertIn('number_Of_Lessons', form.fields)
        self.assertIn('length', form.fields)
        self.assertIn('interval', form.fields)
        self.assertIn('body', form.fields)
        