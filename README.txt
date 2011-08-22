

These are extensions for Django's forms.

Currently this contains the following:

- ForeignKeyChoiceField

    When you have a formset that has a foreign key, Django will
    fire off a new (identical) query to build the choices for
    that field for each form in the formset by default. Using this
    field will allow you to run the query once for the choices and
    re-use that queryset for each form in the formset.

- FormSetView

    Django 1.3's generic views do not include a FormSet view. That's
    what this is. 