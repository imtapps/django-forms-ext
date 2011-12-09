import mock

from django.utils.unittest import TestCase
from django.views.generic import CreateView

from forms_ext.views.generic import FormSetView, MessageFormMixin

__all__ = (
    'MessageFormMixinTests',
    'FormSetViewTests',
)

class TestView(object):

    def form_valid(self, form):
        return "expected_response"

class MessageTestView(MessageFormMixin, TestView):
    request = mock.Mock()

class MessageFormMixinTests(TestCase):
    """
    Just testing mechanics...
    """

    def test_form_valid_returns_super_form_valid(self):
        form = mock.Mock()

        mv = MessageTestView()
        response = mv.form_valid(form)
        self.assertEqual("expected_response", response)

    @mock.patch.object(MessageFormMixin, 'get_success_message')
    @mock.patch('django.contrib.messages.info')
    def test_form_valid_adds_message(self, info, get_message):
        mv = MessageTestView()

        mv.form_valid(mock.Mock())
        info.assert_called_once_with(mv.request, get_message.return_value)


class FormSetViewTests(TestCase):

    def setUp(self):
        self.view = FormSetView()
        self.view.request = mock.Mock()

    def test_subclass_CreateView(self):
        self.assertTrue(issubclass(FormSetView, CreateView))

    def test_set_template_name_suffix_to_formset(self):
        self.assertEqual("_formset", self.view.template_name_suffix)

    @mock.patch('forms_ext.views.generic.FormSetView.render_to_response', mock.Mock())
    @mock.patch('forms_ext.views.generic.FormSetView.get_form')
    @mock.patch('forms_ext.views.generic.FormSetView.get_form_class')
    def test_send_formset_class_to_get_form(self, get_form_class, get_form):
        self.view.get(mock.Mock())

        get_form_class.assert_called_once_with()
        get_form.assert_called_once_with(get_form_class.return_value)

    @mock.patch('forms_ext.views.generic.FormSetView.render_to_response', mock.Mock())
    @mock.patch('forms_ext.views.generic.FormSetView.get_form_class', mock.Mock())
    @mock.patch('forms_ext.views.generic.FormSetView.get_form')
    @mock.patch('forms_ext.views.generic.FormSetView.get_context_data')
    def test_send_form_to_context_data_as_formset(self, get_context_data, get_form):
        self.view.get(mock.Mock())
        get_context_data.assert_called_once_with(formset=get_form.return_value)

    @mock.patch('forms_ext.views.generic.FormSetView.get_form_class', mock.Mock())
    @mock.patch('forms_ext.views.generic.FormSetView.get_form', mock.Mock())
    @mock.patch('forms_ext.views.generic.FormSetView.render_to_response')
    @mock.patch('forms_ext.views.generic.FormSetView.get_context_data')
    def test_send_context_data_to_render_to_response(self, get_context_data, render_to_response):
        self.view.get(mock.Mock())
        render_to_response.assert_called_once_with(get_context_data.return_value)

    @mock.patch('forms_ext.views.generic.FormSetView.get_queryset')
    @mock.patch('django.views.generic.edit.FormMixin.get_form_kwargs')
    def test_send_queryset_with_form_kwargs(self, get_form_kwargs, get_queryset):
        get_form_kwargs.return_value = {'initial': mock.sentinel.initial}

        kwargs = self.view.get_form_kwargs()

        self.assertEqual({
            'queryset': get_queryset.return_value,
            'initial': mock.sentinel.initial,
        }, kwargs)

    @mock.patch('forms_ext.views.generic.FormSetView.render_to_response')
    @mock.patch('forms_ext.views.generic.FormSetView.get_context_data')
    def test_render_response_with_formset_when_form_invalid(self, get_context_data, render_to_response):
        formset = mock.Mock()
        response = self.view.form_invalid(formset)
        get_context_data.assert_called_once_with(formset=formset)
        render_to_response.assert_called_once_with(get_context_data.return_value)
        self.assertEqual(render_to_response.return_value, response)