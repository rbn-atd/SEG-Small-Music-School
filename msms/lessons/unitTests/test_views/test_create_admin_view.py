from django.test import TestCase
from django.urls import reverse
from lessons.forms import CreateNewAdminForm
from lessons.models import User

"""Unit tests for create_admin view"""
class CreateNewAdminViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('create_admin')

        self.form_input={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'username': 'janedoe@example.org',
                'new_password': 'Password123',
                'password_confirmation': 'Password123',
                'admin_type_choice': 'normal_admin',

            }

    def test_create_admin_url(self):
        self.assertEqual(self.url,'/create_admin/')
    
    def test_get_create_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateNewAdminForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_create_admin(self):
        self.form_input['username']='BAD_USERNAME'
        before_count=User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count=User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateNewAdminForm))
        self.assertTrue(form.is_bound)

    def test_successful_create_admin(self):
        before_count=User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count=User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url=reverse('admin_home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_home.html')
        admin = User.objects.get(username='janedoe@example.org')
        self.assertEqual(admin.first_name, 'Jane')
        self.assertEqual(admin.last_name, 'Doe')
        self.assertEqual('Password123', self.form_input['new_password'])
        self.assertEqual(admin.is_staff, True)
        self.assertEqual(admin.is_super_user, False)

 




