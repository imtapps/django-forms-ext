# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from lettuce import step, world
from example.sample.models import EyeColor, Person

@step(u'Given the eye colors')
def given_the_eye_colors(step):
    for color in step.hashes:
        EyeColor.objects.create(**color)

@step(u'And post the form with')
def post_form(step):
    response = world.browser.post(reverse('querysetchoice'), step.hashes.first)
    assert response.status_code == 302, response.content

@step(u'Then I expect a person with the name of "([^"]*)" to have a second_eye_color of "([^"]*)"')
def verify_person_has_second_eye_color_as_int(step, name, eye_color):
    step.scenario.person = Person.objects.get(name=name, second_eye_color=eye_color)

@step(u'And an eye_color of the EyeColor model instance for pk "([^"]*)"')
def verify_person_has_eye_color_as_model_pk(step, eye_color):
    assert step.scenario.person.eye_color == EyeColor.objects.get(pk=eye_color)
