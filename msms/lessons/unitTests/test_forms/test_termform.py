from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Term
from django import forms
from lessons.forms import TermForm


"""Unit tests for the user model"""
class TermFormTestCase(TestCase):
    def setUp(self):
        pass