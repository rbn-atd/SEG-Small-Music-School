from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import User


"""Unit tests for the user model"""
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(
            'johndoe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123'
        )

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_firstname_cannot_be_blank(self):
        self.user.first_name=''
        self._assert_user_is_invalid()

    def test_firstname_may_already_exist(self):
        self._create_second_user()
        self.user.first_name='Jane'
        self._assert_user_is_valid

    def test_firstname_can_be_50_chars(self):
        self.user.first_name='x'*50
        self._assert_user_is_valid()
        
    def first_name_cant_be_over_50_chars(self):
        self.user.first_name='x'*51
        self._assert_user_is_invalid()

    def test_lastname_cannot_be_blank(self):
        self.user.last_name=''
        self._assert_user_is_invalid()

    def test_lastname_may_already_exist(self):
        self._create_second_user()
        self.user.last_name='Dog'
        self._assert_user_is_valid

    def last_name_can_be_50_chars(self):
        self.user.last_name='x'*50
        self._assert_user_is_valid()

    def last_name_cant_be_over_50_chars(self):
        self.user.last_name='x'*51
        self._assert_user_is_invalid()

    def test_email_is_unique(self):
        self._create_second_user()
        self.user.username = 'janedog@example.org'
        self._assert_user_is_invalid()

    def test_email_contains_at_symbol(self):
        self.user.username = 'johndoe.org'
        self._assert_user_is_invalid()

    def test_email_contains_only_one_at(self):
        self.user.username = 'johndoe@@example.org'
        self._assert_user_is_invalid()

    def test_email_has_name_before_at(self):
        self.user.username = '@example.org'
        self._assert_user_is_invalid()

    def test_email_has_domain_after_at(self):
        self.user.username = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    # Test for if user is of user_type student
    def test_user_type_is_student(self):
        self.user.user_type=1
        self._assert_user_is_valid

    #  Test user may be an admin
    def test_user_type_can_be_admin(self):
        self.user.user_type=2
        self._assert_user_is_valid

    # Test user may be a director
    def test_user_type_can_be_director(self):
        self.user.user_type=3
        self._assert_user_is_valid

    def _create_second_user(self):
        self.user_2= User.objects.create_user(
            'janedog@example.org',
            first_name='Jane',
            last_name='Dog',
            password='Password123'
        )

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')
    
    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
    