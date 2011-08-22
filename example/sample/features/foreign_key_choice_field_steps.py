from lettuce import step, world

@step(u'Given a page with "(.*)" people forms')
def setup_page(step, form_count):
    world.form_count = int(form_count)

@step(u'Then I expect there to be "(.*)" queries executed')
def assert_number_of_queries_executed(step, query_count):
    message = "Queries Executed: %s, Max Queries Expected %s" % (world.number_of_queries, query_count)
    assert world.number_of_queries == int(query_count), message


