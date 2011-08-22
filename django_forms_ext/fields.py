from django import forms
from django.core.validators import EMPTY_VALUES

__all__ = (
    'ForeignKeyChoiceField',
)

class ForeignKeyChoiceField(forms.ModelChoiceField):

    def __init__(self, model_class, *args, **kwargs):
        self.model_class = model_class
        super(ForeignKeyChoiceField, self).__init__(model_class.objects.none(), *args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        return self.model_class(pk=value)
