from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Term
import datetime

"""Unit tests for the term model"""
class TermModelTestCase(TestCase):
    def setUp(self):
        self.term= Term(
            term_number=1,
            start_date=datetime.date(2022,10,1),
            end_date=datetime.date(2022,11,1)
        )
    
    def test_valid_term(self):
        try:
            self.term.full_clean()
        except ValidationError:
            self.fail("Test term should be valid")

    def test_end_date_is_after_start_date(self):
        self.term.end_date = datetime.date(2021,11,1)
        if self.term.end_date<self.term.start_date:
            with self.assertRaises(ValidationError):
                self.term.full_clean()

    def test_term_number_is_unique(self):
        self.term.term_number=2
        self._create_second_term()
        with self.assertRaises(ValidationError):
            self.term.full_clean()

    def test_term_number_cannot_be_blank(self):
        self.term.term_number=None
        with self.assertRaises(ValidationError):
            self.term.full_clean()


    def test_term_dates_are_not_blank(self):
        self.term.term_number=None
        with self.assertRaises(ValidationError):
            self.term.full_clean()
    def test_term_dates_cannot_overlap(self):
        pass

    def _create_second_term(self):
        Term(
            term_number=2,
            start_date=datetime.date(2022,12,1),
            end_date=datetime.date(2023,1,1)
        )