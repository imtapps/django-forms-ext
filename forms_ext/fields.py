
from django import forms
from django.core.validators import EMPTY_VALUES
from django.forms.models import ModelChoiceField

from forms_ext.validators import EachSequenceItemLengthValidator

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
        field_name = self.to_field_name or 'pk'
        return self.model_class.objects.get(**{field_name:value})

class CommaSeparatedField(forms.CharField):
    description = "Comma-separated strings"

    def __init__(self, max_item_length, *args, **kwargs):
        super(CommaSeparatedField, self).__init__(*args, **kwargs)
        self.validators.append(EachSequenceItemLengthValidator(max_item_length))

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return u''
        if isinstance(value, (list, tuple)):
            return value
        return value.split(',')

    def prepare_value(self, value):
        if isinstance(value, basestring):
            return value
        return value and ','.join(v for v in value if v)

class QuerysetChoiceField(ModelChoiceField):

    def to_python(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
