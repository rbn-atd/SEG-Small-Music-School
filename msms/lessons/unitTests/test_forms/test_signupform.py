from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import User
from django import forms
from lessons.forms import SignUpForm
from django.contrib.auth.hashers import check_password

"""Unit tests for the user model"""
class SignUpFormTestCase(TestCase):
    def setUp(self):
            self.form_input={
                'user_type': 1,
                'first_name': 'Jane',
                'last_name': 'Dog',
                'username': 'janedog@example.org',
                'new_password': 'Password123',
                'password_confirmation': 'Password123'
            }
                
    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_all_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        email_field = form.fields['username']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'bad'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_has_uppercase_letter(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_password_has_lowercase_letter(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_has_number(self):
        self.form_input['new_password'] = 'PasswordWOW'
        self.form_input['password_confirmation'] = 'PasswordWOW'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_and_confirmation_are_equal(self):
        self.form_input['password_confirmation'] = 'NotTheSame0'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input)
        before_count=User.objects.count()
        form.save()
        after_count= User.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = User.objects.get(username ='janedog@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Dog')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
            