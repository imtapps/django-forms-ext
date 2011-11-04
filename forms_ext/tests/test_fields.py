
import mock

from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.unittest import TestCase

from forms_ext import fields

__all__ = (
    'ForeignKeyChoiceFieldTests',
    'CommaSeparatedFieldTests',
    'QuerysetChoiceFieldTests',
)

class ForeignKeyChoiceFieldTests(TestCase):

    def test_sets_model_class_in_init(self):
        model_class = mock.Mock()
        field = fields.ForeignKeyChoiceField(model_class)
        self.assertEqual(field.model_class, model_class)

    def test_passes_empty_queryset_into_super_on_init(self):
        model_class = mock.Mock()
        with mock.patch('django.forms.ModelChoiceField.__init__') as init_patch:
            fields.ForeignKeyChoiceField(model_class)
        init_patch.assert_called_once_with(model_class.objects.none.return_value)

    def test_returns_none_from_to_python_for_empty_values(self):
        field = fields.ForeignKeyChoiceField(mock.Mock())

        for empty_value in EMPTY_VALUES:
            self.assertEqual(None, field.to_python(empty_value))

        if not EMPTY_VALUES:
            self.fail("this test will not work without EMPTY_VALUES")

    def test_instantiates_the_model_class_with_the_value_as_pk_in_to_python(self):
        model_class = mock.Mock()
        field = fields.ForeignKeyChoiceField(model_class)
        instance = field.to_python(123)
        model_class.objects.get.assert_called_once_with(pk=123)
        self.assertEqual(model_class.objects.get.return_value, instance)


class CSVTestForm(forms.Form):
    csv_field = fields.CommaSeparatedField(max_item_length=3, required=False)

class CommaSeparatedFieldTests(TestCase):

    def setUp(self):
        self.field = fields.CommaSeparatedField(max_item_length=3, required=False)
        self.field_input = "abc,123,xyz"
        self.expected_output = ['abc', '123', 'xyz']

    def test_to_python_separates_string_on_commas(self):
        self.assertEqual(['abc', '123'], self.field.to_python('abc,123'))

    def test_to_python_returns_empty_string_when_value_given_is_none(self):
        self.assertEqual('', self.field.to_python(None))

    def test_to_python_returns_empty_string_when_value_given_is_empty_string(self):
        self.assertEqual('', self.field.to_python(''))

    def test_to_python_returns_empty_string_when_value_given_is_empty_list(self):
        self.assertEqual('', self.field.to_python([]))

    def test_to_python_returns_empty_string_when_value_given_is_empty_tuple(self):
        self.assertEqual('', self.field.to_python(()))

    def test_to_python_returns_empty_string_when_value_given_is_empty_dict(self):
        self.assertEqual('', self.field.to_python({}))

    def test_to_python_returns_list_when_list_was_given_as_input(self):
        expected_value = ['AAA', 'BBB']
        self.assertEqual(expected_value, self.field.to_python(expected_value))

    def test_to_python_returns_tuple_when_tuple_was_given_as_input(self):
        expected_value = ('AAA', 'BBB')
        self.assertEqual(expected_value, self.field.to_python(expected_value))

    def test_prepare_value_turns_list_into_comma_separated_string_for_display(self):
        self.assertEqual("1,2,3", self.field.prepare_value(['1', '2', '3']))

    def test_prepare_value_ignores_csv_values_for_display_that_evaluate_falsy(self):
        self.assertEqual("one,two", self.field.prepare_value(['one', None, '', [], (), {}, 'two']))

    def test_prepare_value_does_not_join_items_for_display_when_already_string_value(self):
        self.assertEqual("1,2,3", self.field.prepare_value("1,2,3"))

    def test_prepare_value_does_not_join_items_for_display_when_none(self):
        self.assertEqual(None, self.field.prepare_value(None))

    def test_validates_max_length_of_each_comma_separated_value(self):
        form = CSVTestForm({'csv_field': 'toolongvalue,anothertoolongvalue'})
        self.assertFalse(form.is_valid())

class QuerysetChoiceFieldTests(TestCase):

    def setUp(self):
        self.mock = mock.Mock(spec=fields.QuerysetChoiceField)

    def test_extends_djangos_model_choice_field(self):
        self.assertTrue(issubclass(fields.QuerysetChoiceField, forms.ModelChoiceField))

    def test_to_python_returns_integer_value(self):
        result = fields.QuerysetChoiceField.to_python(self.mock, '123')
        self.assertEqual(123, result)

    def test_to_python_returns_none_when_value_is_none(self):
        result = fields.QuerysetChoiceField.to_python(self.mock, None)
        self.assertEqual(None, result)

    def test_to_python_returns_none_when_value_is_invalid(self):
        result = fields.QuerysetChoiceField.to_python(self.mock, "asdf")
        self.assertEqual(None, result)

