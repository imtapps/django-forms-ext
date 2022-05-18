from django.conf.urls import patterns, url

from sample import views

urlpatterns = patterns(
    '',
    url(r'^few-queries$', views.FewQueries.as_view(), name="few_queries"),
    url(r'^many-queries$', views.ManyQueries.as_view(), name="many_queries"),
    url(r'^simple-formset-view$', views.SimpleFormsetView.as_view(), name="simple"),
    url(r'^queryset-choice-view$', views.QuerysetChoiceFieldView.as_view(), name="querysetchoice"),
)
