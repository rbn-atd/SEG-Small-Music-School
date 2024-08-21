from pickle import NONE
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Request
from lessons.models import User

"""Unit tests for the request model"""
class RequestModelTestCase(TestCase):
    def setUp(self):
        self.new_user= User.objects.create_user(
            'johndoe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123'
        )
        
        self.request= Request.objects.create(
            user = self.new_user,
            availability = ['Monday'],
            number_Of_Lessons = '1',
            length = '30 mins',
            interval = 'every week',
            body = 'Test message',
            status = False,
        )

    def test_valid_request(self):
        self._assert_request_is_valid()
        
    def test_availability_can_have_multiple_selection(self):
        self.request.availability = ['Monday','Tuesday','Friday']
        self._assert_request_is_valid()   
        
    def test_number_Of_Lessons_cannot_be_blank(self):
        self.request.number_Of_Lessons=''
        self._assert_request_is_invalid()
        
    def test_length_cannot_be_blank(self):
        self.request.length=''
        self._assert_request_is_invalid()  
    
    def test_interval_cannot_be_blank(self):
        self.request.interval=''
        self._assert_request_is_invalid()      

    def test_body_can_be_blank(self):
        self.request.body=''
        self._assert_request_is_valid() 
        
    def body_can_be_200_chars(self):
        self.request.body='x'*200
        self._assert_request_is_valid() 

    def body_cant_be_over_200_chars(self):
        self.request.body='x'*201
        self._assert_request_is_invalid() 

    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except (ValidationError):
            self.fail('Test request should be valid')
    
    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.full_clean()