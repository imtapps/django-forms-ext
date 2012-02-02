import mock

from django import test
from django.views.generic import CreateView

from forms_ext.views.generic import FormSetView, MessageFormMixin, SearchFormView

__all__ = (
    'MessageFormMixinTests',
    'FormSetViewTests',
    'SearchFormViewTests',
)

class TestView(object):

    def form_valid(self, form):
        return "expected_response"


class MessageTestView(MessageFormMixin, TestView):
    request = mock.Mock()


class MessageFormMixinTests(test.TestCase):
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


class FormSetViewTests(test.TestCase):

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


class SearchFormViewTests(test.TestCase):

    def _get_view(self, request=None):
        return SearchFormView(request=request)

    def test_subclasses_template_response_mixin(self):
        from django.views.generic.base import TemplateResponseMixin
        self.assertTrue(issubclass(SearchFormView, TemplateResponseMixin))

    def test_subclasses_form_mixin(self):
        from django.views.generic.edit import FormMixin
        self.assertTrue(issubclass(SearchFormView, FormMixin))

    def test_subclasses_view(self):
        from django.views.generic.base import View
        self.assertTrue(issubclass(SearchFormView, View))

    @mock.patch.object(SearchFormView, 'form_valid', mock.Mock())
    @mock.patch.object(SearchFormView, 'get_form_class')
    def test_get_method_gets_form_class(self, get_form_class):
        request = test.RequestFactory().get('/')
        view = self._get_view(request)
        view.get(request)

        get_form_class.assert_called_once_with()

    @mock.patch.object(SearchFormView, 'form_valid', mock.Mock())
    @mock.patch.object(SearchFormView, 'get_form')
    @mock.patch.object(SearchFormView, 'get_form_class')
    def test_get_method_creates_form_with_form_class(self, get_form_class, get_form):
        request = test.RequestFactory().get('/')
        view = self._get_view(request)
        view.get(request)

        get_form.assert_called_once_with(get_form_class.return_value)

    @mock.patch.object(SearchFormView, 'form_valid')
    @mock.patch.object(SearchFormView, 'get_form')
    def test_get_method_returns_form_valid_when_valid(self, get_form, form_valid):
        form = get_form.return_value
        form.is_valid.return_value = True

        request = test.RequestFactory().get('/')
        view = self._get_view(request)
        response = view.get(request)

        self.assertEqual(form_valid.return_value, response)
        form_valid.assert_called_once_with(form)

    @mock.patch.object(SearchFormView, 'form_invalid')
    @mock.patch.object(SearchFormView, 'get_form')
    def test_get_method_returns_form_invalid_when_not_valid(self, get_form, form_invalid):
        form = get_form.return_value
        form.is_valid.return_value = False

        request = test.RequestFactory().get('/')
        view = self._get_view(request)
        response = view.get(request)

        self.assertEqual(form_invalid.return_value, response)
        form_invalid.assert_called_once_with(form)

    @mock.patch.object(SearchFormView, 'get_initial')
    def test_get_form_kwargs_returns_initial_and_get_data(self, get_initial):
        request = test.RequestFactory().get('/', data={'form_data': 'something'})
        view = self._get_view(request)

        form_kwargs = view.get_form_kwargs()
        self.assertEqual({
            'initial': get_initial.return_value,
            'data': request.GET,
        }, form_kwargs)
        get_initial.assert_called_once_with()

    @mock.patch.object(SearchFormView, 'get_initial')
    def test_get_form_kwargs_returns_initial_and_none_for_data(self, get_initial):
        request = test.RequestFactory().get('/')
        view = self._get_view(request)

        form_kwargs = view.get_form_kwargs()
        self.assertEqual({
            'initial': get_initial.return_value,
            'data': None,
        }, form_kwargs)
        get_initial.assert_called_once_with()
