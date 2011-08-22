
from django.core.exceptions import ValidationError
from django.utils.unittest import TestCase

from forms_ext import fields

__all__ = (
    'EachSequenceItemLengthValidatorTests',
)

class EachSequenceItemLengthValidatorTests(TestCase):

    def test_raises_validation_error_when_item_in_list_exceeds_max_value(self):
        validator = fields.EachSequenceItemLengthValidator(5)
        with self.assertRaises(ValidationError) as e:
            validator(["abcdef"])
        expected_message = u'Ensure each item is less than or equal to 5 characters.'
        self.assertEqual(expected_message, e.exception.messages[0])

    def test_returns_none_when_all_items_less_than_max_length(self):
        validator = fields.EachSequenceItemLengthValidator(3)
        self.assertEqual(None, validator(["abc", "xyz", "123"]))