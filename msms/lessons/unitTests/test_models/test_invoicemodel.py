from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Invoice, Request


"""Unit tests for the invoice model"""
class InvoiceModelTestCase(TestCase):
    def setUp(self):
        # request = ,
        accepting_admin = 'testadmin@example.org',
        cost = 15,
        paid = False,
        invoice_number = '005-002'

    def test_valid_invoice(self):
        pass

    def test_invoice_has_associated_request(self):
        pass

    def test_accepting_admin_cannot_be_blank(self):
        pass
