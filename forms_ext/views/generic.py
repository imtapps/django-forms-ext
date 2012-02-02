
from django.contrib import messages
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, FormMixin

__all__ = (
    'MessageFormMixin',
    'FormSetView',
    'SearchFormView',
)

class MessageFormMixin(object):
    """
    Mixin to use with Django's generic form views to add
    a message using the django.contrib.messages app on
    a successful form post.
    """

    def form_valid(self, form):
        response = super(MessageFormMixin, self).form_valid(form)
        messages.info(self.request, self.get_success_message())
        return response

    def get_success_message(self):
        return "Changes saved successfully."


# todo: someday make 'MessageViews' available for FormView, CreateView, UpdateView, and DeleteView
# todo: also make the MessageFormMixin have a 'add_message' method so it is easy to override message type.

class FormSetView(MessageFormMixin, CreateView):
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

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))


class SearchFormView(TemplateResponseMixin, FormMixin, View):
    """
    Search form executes real action using form's GET data.

    To make the view useful, generally you'll override the
    form_valid method to execute your search and return the results
    in a template.
    """

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        return {
            'initial': self.get_initial(),
            'data': self.request.GET or None,
        }
