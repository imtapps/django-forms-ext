
import mock

from django import forms
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.unittest import TestCase

from forms_ext import fields

__all__ = (
    'ForeignKeyChoiceFieldTests',
    'CommaSeparatedFieldTests',
    'QuerysetChoiceFieldTests',
    'USSocialSecurityFieldTests',
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

class USSocialSecurityFieldTests(TestCase):

    def setUp(self):
        self.field = fields.USSocialSecurityNumberField()

    def test_returns_empty_string_when_value_is_none(self):
        field = fields.USSocialSecurityNumberField(required=False)
        self.assertEqual('', field.clean(None))

    def test_returns_empty_string_when_value_is_empty_string(self):
        field = fields.USSocialSecurityNumberField(required=False)
        self.assertEqual('', field.clean(''))

    def test_raises_required_message_when_value_is_required(self):
        field = fields.USSocialSecurityNumberField()
        with self.assertRaises(ValidationError) as e:
            field.clean(None)
        self.assertEqual([field.error_messages['required']], e.exception.messages)

    def test_returns_value_when_valid_social_security_number(self):
        ssn = "123-45-6789"
        self.assertEqual(ssn, self.field.clean(ssn))

    def test_forces_number_to_dashes_when_valid_and_not_remove_dashes(self):
        ssn = "123456789"
        self.assertEqual("123-45-6789", self.field.clean(ssn))

    def test_forces_number_to_no_dashes_when_valid_and_remove_dashes(self):
        field = fields.USSocialSecurityNumberField(no_hyphens=True)
        ssn = "123-45-6789"
        self.assertEqual("123456789", field.clean(ssn))

    def test_is_not_valid_when_any_blocks_are_all_zero(self):
        with self.assertRaises(ValidationError):
            self.field.clean("000-12-1234")

        with self.assertRaises(ValidationError):
            self.field.clean("123-00-1234")

        with self.assertRaises(ValidationError):
            self.field.clean("123-12-0000")

    def test_is_not_valid_when_area_is_666(self):
        with self.assertRaises(ValidationError):
            self.field.clean("666-12-1234")

    def test_is_not_valid_when_in_promotional_range(self):
        # 987-65-(4320 - 4329) is invalid
        for x in range(4320, 4330):
            with self.assertRaises(ValidationError):
                self.field.clean("987-65-{area}".format(area=x))
        lower_bound = "987-65-4319"
        upper_bound = "987-65-4330"
        self.assertEqual(lower_bound, self.field.clean(lower_bound))
        self.assertEqual(upper_bound, self.field.clean(upper_bound))

    def test_078_05_1120_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.field.clean("078-05-1120")

    def test_219_09_9999_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.field.clean("219-09-9999")
