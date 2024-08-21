from django.test import TestCase
from lessons.models import AdminStaff
from django import forms
from lessons.forms import CreateNewAdminForm


"""Unit tests for the CreateAdminForm"""
class CreateAdminFormTestCase(TestCase):
    def setUp(self):
            self.form_input={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'username': 'janedoe@example.org',
                'new_password': 'Password123',
                'password_confirmation': 'Password123',
                'admin_type_choice': 'normal_admin',
            }
                
    def test_valid_create_admin_form(self):
        form = CreateNewAdminForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_all_fields(self):
        form = CreateNewAdminForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        # self.assertIn('username', form.fields)
        username_email_field = form.fields['username']
        self.assertTrue(isinstance(username_email_field, forms.EmailField))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'BAD_USERNAME'
        form = CreateNewAdminForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_is_the_same_as_default(self):
        self.form_input['new_password'] = 'Password123'
        self.form_input['password_confirmation'] = 'Password123'
        self.assertEqual(self.form_input['new_password'], 'Password123')
        form = CreateNewAdminForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_password_and_confirmation_are_not_equal_to_default(self):
        self.form_input['new_password'] = 'NotTheSame0'
        self.form_input['password_confirmation'] = 'NotTheSame0'
        self.assertNotEqual(self.form_input['new_password'], 'Password123')
        form = CreateNewAdminForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = CreateNewAdminForm(data=self.form_input)
        before_count=AdminStaff.objects.count()
        form.save()
        after_count= AdminStaff.objects.count()
        self.assertEqual(after_count, before_count+1)
        admin = AdminStaff.objects.get(username ='janedoe@example.org')
        self.assertEqual(admin.first_name, 'Jane')
        self.assertEqual(admin.last_name, 'Doe')
        self.assertEqual('Password123', self.form_input['new_password'])
        
            