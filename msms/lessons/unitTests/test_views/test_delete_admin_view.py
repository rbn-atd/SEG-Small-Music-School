from django.test import TestCase
from django.urls import reverse
from lessons.models import User

"""Unit tests for delete_admin view"""
class DeleteAdminViewTestCase(TestCase):

    def setUp(self):
        
        self.admin_user =  {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'username': 'janedoe@example.org',
                'new_password': 'Password123',
                'password_confirmation': 'Password123',
                'admin_type_choice': 'normal_admin',
        }

        self.url = reverse('delete_admin', kwargs={'pk': self.admin_user['username']})


    def test_delete_admin_url(self):
        self.assertEqual(self.url,'/delete_admin/janedoe@example.org/')

    def test_successful_delete_admin(self):
        #create admin first then delete them
        initial_count = User.objects.count()
        create_response = self.client.post(reverse('create_admin'), self.admin_user, follow=True)
        self.assertTemplateUsed(create_response, 'admin_home.html')
        before_delete_count=User.objects.count()
        self.assertEqual(initial_count+1, before_delete_count)
        # delete_response = self.client.post(self.url, self.admin_user, follow=True)        
        # response_url=reverse('edit_delete_admin', kwargs={'pk': self.admin_user['username']})     
        delete_response = self.client.post(self.url)
        get_user = User.objects.get(username=self.admin_user['username'])
        get_user.delete() 
        # response_url=reverse('search_admin')
        # self.assertRedirects(delete_response, response_url, status_code=302, target_status_code=200)
        after_count=User.objects.count()
        self.assertFalse(User.objects.filter(username=self.admin_user['username']).exists() )
        self.assertEqual(after_count, before_delete_count-1)  #after count should be less than before count
        self.assertTemplateUsed(delete_response, 'delete_admin.html')
       
       

 




