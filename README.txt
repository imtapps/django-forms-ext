

These are extensions for Django's forms.

Currently this contains the following:

Fields
=========

- ForeignKeyChoiceField

    When you have a formset that has a foreign key, Django will
    fire off a new (identical) query to build the choices for
    that field for each form in the formset by default. Using this
    field will allow you to run the query once for the choices and
    re-use that queryset for each form in the formset.

- CommaSeparatedField

    Django has a comma separated integer field, but not just strings.
    Stupid, I know... we created one for use with strings

- QuerysetChoiceField

    When you want to build a select box with a queryset but don't want
    a model instance when saving, use this thing.

Views
=========
- FormSetView

    Django 1.3's generic views do not include a FormSet view. That's
    what this is. 