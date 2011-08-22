import mock

from django.utils.unittest import TestCase
from django.core.validators import EMPTY_VALUES

from django_forms_ext.fields import ForeignKeyChoiceField

__all__ = (
    'ForeignKeyChoiceFieldTests',
)

class ForeignKeyChoiceFieldTests(TestCase):

    def test_sets_model_class_in_init(self):
        model_class = mock.Mock()
        field = ForeignKeyChoiceField(model_class)
        self.assertEqual(field.model_class, model_class)

    def test_passes_empty_queryset_into_super_on_init(self):
        model_class = mock.Mock()
        with mock.patch('django.forms.ModelChoiceField.__init__') as init_patch:
            ForeignKeyChoiceField(model_class)
        init_patch.assert_called_once_with(model_class.objects.none.return_value)

    def test_returns_none_from_to_python_for_empty_values(self):
        field = ForeignKeyChoiceField(mock.Mock())

        for empty_value in EMPTY_VALUES:
            self.assertEqual(None, field.to_python(empty_value))

        if not EMPTY_VALUES:
            self.fail("this test will not work without EMPTY_VALUES")

    def test_instantiates_the_model_class_with_the_value_as_pk_in_to_python(self):
        model_class = mock.Mock()
        field = ForeignKeyChoiceField(model_class)
        instance = field.to_python(123)
        model_class.assert_called_once_with(pk=123)
        self.assertEqual(model_class.return_value, instance)
