from lettuce import before, step, world

from django.db import connection
from django.core.management import call_command
from django.test.client import Client
from django.core.urlresolvers import reverse

@before.all
def setup_test_database():
    connection.creation.create_test_db(verbosity=1, autoclobber=True)

@before.each_scenario
def clean_db(scenario):
    call_command('flush', interactive=False, verbosity=0)

@step(u'(?:Given|And) a web browser')
def given_a_web_browser(step):
    world.browser = Client()

@step(u'When I visit the "(.*)" page')
def when_i_visit_the_page(step, page_name):
    with capture_queries_executed as context:
        step.scenario.response = world.browser.get(reverse(page_name))

    step.scenario.number_of_queries = context.executed

from django.db import connection, reset_queries
from django.core.signals import request_started

class QueryCountContextManager(object):
    """
    Adapted from Django's _AssertNumQueries test class
    """
    executed = 0

    def __init__(self, conn=None):
        self.connection = conn or connection
        self.executed = 0

    def __enter__(self):
        self.old_debug_cursor = self.connection.use_debug_cursor
        self.connection.use_debug_cursor = True
        self.starting_queries = len(self.connection.queries)
        request_started.disconnect(reset_queries)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.use_debug_cursor = self.old_debug_cursor
        request_started.connect(reset_queries)
        if exc_type is not None:
            return

        final_queries = len(self.connection.queries)
        self.executed = final_queries - self.starting_queries

capture_queries_executed = QueryCountContextManager()




