
from django.core.validators import MaxLengthValidator

__all__ = ('EachSequenceItemLengthValidator',)

class EachSequenceItemLengthValidator(object):
    message = u'Ensure each item is less than or equal to %(limit_value)s characters.'

    def __init__(self, max_item_length):
        self.max_length_validator = MaxLengthValidator(max_item_length)
        self.max_length_validator.message = self.message

    def __call__(self, value_sequence):
        for value in value_sequence:
            self.max_length_validator(value)