from django.contrib import messages
from django.views.generic.edit import CreateView, FormMixin

__all__ = (
    'FormSetView',
)

class FormSetView(CreateView):
    """
    A view that processes formsets instead of forms.

    Only difference really is that we're sending 'formset' into
    template instead of 'form' and we need to give the formset
    a queryset, not an instance. The rest of the view behaves
    close enough to a regular form that we can use it as such.

    TODO: cleanup references to "form" and replace with "formset"

    """
    object = None
    model = None
    template_name_suffix = '_formset'

    def get(self, request, *args, **kwargs):
        formset_class = self.get_form_class()
        formset = self.get_form(formset_class)
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the formset.
        """
        kwargs = FormMixin.get_form_kwargs(self)
        kwargs.update({'queryset': self.get_queryset()})
        return kwargs

    def form_valid(self, formset):
        formset.save()
        messages.info(self.request, "%s have been updated successfully." % self.model._meta.verbose_name_plural)
        return FormMixin.form_valid(self, formset)

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))
