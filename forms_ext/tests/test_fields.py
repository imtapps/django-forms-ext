
import mock

from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.unittest import TestCase

from forms_ext import fields

__all__ = (
    'ForeignKeyChoiceFieldTests',
    'CommaSeparatedFieldTests',
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
        model_class.assert_called_once_with(pk=123)
        self.assertEqual(model_class.return_value, instance)


class CSVTestForm(forms.Form):
    csv_field = fields.CommaSeparatedField(max_item_length=3, required=False)

class CommaSeparatedFieldTests(TestCase):

    def setUp(self):
        self.field_input = "abc,123,xyz"
        self.expected_output = ['abc', '123', 'xyz']

    def test_separates_string_on_commas(self):
        form = CSVTestForm({'csv_field': self.field_input})
        form.is_valid()

        self.assertEqual(self.expected_output, form.cleaned_data['csv_field'])

    def test_returns_empty_string_when_value_given_is_none(self):
        form = CSVTestForm({'csv_field': None})
        form.is_valid()

        self.assertEqual('', form.cleaned_data['csv_field'])

    def test_returns_empty_string_when_value_given_is_empty_string(self):
        form = CSVTestForm({'csv_field': ''})
        form.is_valid()

        self.assertEqual('', form.cleaned_data['csv_field'])

    def test_returns_empty_string_when_value_given_is_empty_list(self):
        form = CSVTestForm({'csv_field': []})
        form.is_valid()

        self.assertEqual('', form.cleaned_data['csv_field'])

    def test_returns_empty_string_when_value_given_is_empty_tuple(self):
        form = CSVTestForm({'csv_field': ()})
        form.is_valid()

        self.assertEqual('', form.cleaned_data['csv_field'])

    def test_returns_empty_string_when_value_given_is_empty_dict(self):
        form = CSVTestForm({'csv_field': {}})
        form.is_valid()

        self.assertEqual('', form.cleaned_data['csv_field'])

    def test_turns_list_into_comma_separated_string_for_display(self):
        form = CSVTestForm(initial={'csv_field': ['1', '2', '3']})
        self.assertEqual("1,2,3", form['csv_field'].value())

    def test_ignores_csv_values_for_display_that_evaluate_falsy(self):
        form = CSVTestForm(initial={'csv_field': ['one', None, '', [], (), {}, 'two']})
        self.assertEqual("one,two", form['csv_field'].value())

    def test_does_not_join_items_for_display_when_already_string_value(self):
        form = CSVTestForm(initial={'csv_field': "one,two"})
        self.assertEqual("one,two", form['csv_field'].value())

    def test_does_not_join_items_for_display_when_none(self):
        form = CSVTestForm(initial={'csv_field': None})
        self.assertEqual(None, form['csv_field'].value())

    def test_validates_max_length_of_each_comma_separated_value(self):
        form = CSVTestForm({'csv_field': 'toolongvalue,anothertoolongvalue'})
        self.assertFalse(form.is_valid())
