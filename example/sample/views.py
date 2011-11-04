
from django import forms
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from forms_ext.views.generic import FormSetView
from forms_ext.fields import ForeignKeyChoiceField, QuerysetChoiceField

from sample import models

class PersonForm(forms.ModelForm):
    eye_color = ForeignKeyChoiceField(models.EyeColor)

    class Meta(object):
        model = models.Person

class PersonFormSet(forms.models.BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super(PersonFormSet, self).__init__(*args, **kwargs)

        eye_colors = [('', '------')]
        eye_colors.extend([(c.pk, c.name) for c in models.EyeColor.objects.all()])
        for form in self.forms:
            form.fields['eye_color'].choices = eye_colors

class FewQueries(FormSetView):
    model = models.Person
    form_class = forms.models.modelformset_factory(model, form=PersonForm, formset=PersonFormSet, extra=10)

class ManyQueries(FormSetView):
    model = models.Person
    form_class = forms.models.modelformset_factory(model, extra=10)

class SimpleFormsetView(FormSetView):
    model = models.Person
    form_class = forms.models.modelformset_factory(model)

class QuerysetChoiceFieldForm(forms.ModelForm):
    second_eye_color = QuerysetChoiceField(queryset=models.EyeColor.objects.all())

    class Meta(object):
        model = models.Person

class QuerysetChoiceFieldView(CreateView):
    form_class = QuerysetChoiceFieldForm
    template_name = 'sample/form.html'
    def get_success_url(self):
        return reverse('querysetchoice')
