
import re

from django import forms
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from forms_ext.validators import EachSequenceItemLengthValidator

__all__ = (
    'ForeignKeyChoiceField',
)

zeros_re = re.compile('^0+$')
ssn_re = re.compile(r'^(?P<area>\d{3})[-\ ]?(?P<group>\d{2})[-\ ]?(?P<serial>\d{4})$')

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


class USSocialSecurityNumberField(Field):
    """
    A United States Social Security number.

    Checks the following rules to determine whether the number is valid:

        * Conforms to the XXX-XX-XXXX format.
        * No group consists entirely of zeroes.
        * The leading group is not "666" (block "666" will never be allocated).
        * The number is not in the promotional block 987-65-4320 through
          987-65-4329, which are permanently invalid.
        * The number is not one known to be invalid due to otherwise widespread
          promotional use or distribution (e.g., the Woolworth's number or the
          1962 promotional number).

    # Note: submitted patch to django: https://code.djangoproject.com/ticket/17591
    # remove if it makes its way into the main codebase.
    """

    default_error_messages = {
        'invalid': _('Enter a valid U.S. Social Security number in XXX-XX-XXXX format.'),
    }

    def __init__(self, *args, **kwargs):
        self.no_hyphens = kwargs.pop("no_hyphens", False)
        super(USSocialSecurityNumberField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(USSocialSecurityNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''

        ssn_parts = self._get_ssn_parts(value)
        if self._is_invalid_ssn(ssn_parts):
            self._raise_invalid()
        return self._get_formatted_ssn(ssn_parts)

    def _is_invalid_ssn(self, ssn_parts):
        return any([
            self._has_zero_blocks(**ssn_parts),
            self._is_invalid_area(ssn_parts['area']),
            self._is_in_promotional_range(**ssn_parts),
            self._is_known_invalid(**ssn_parts),
        ])

    def _get_formatted_ssn(self, ssn_parts):
        ssn = "{area}-{group}-{serial}".format(**ssn_parts)
        if self.no_hyphens:
            ssn = ssn.replace('-', '')
        return ssn

    def _get_ssn_parts(self, value):
        m = ssn_re.match(value)
        if not m:
            self._raise_invalid()
        return m.groupdict()

    def _raise_invalid(self):
        raise ValidationError(self.error_messages['invalid'])

    def _has_zero_blocks(self, area, group, serial):
        return any([self._is_all_zeros(p) for p in (area, group, serial)])

    def _is_all_zeros(self, part):
        return zeros_re.match(part)

    def _is_invalid_area(self, area):
        return bool(area == '666')

    def _is_in_promotional_range(self, area, group, serial):
        return bool(area == '987' and group == '65' and 4320 <= int(serial) <= 4329)

    def _is_known_invalid(self, area, group, serial):
        return any([
            bool(area == '078' and group == '05' and serial == '1120'),
            bool(area == '219' and group == '09' and serial == '9999'),
        ])