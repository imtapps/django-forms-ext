from lettuce import step, world

@step(u'(?:Given|And) a page with "(.*)" people forms')
def setup_page(step, form_count):
    step.scenario.form_count = int(form_count)

@step(u'Then I expect there to be "(.*)" queries executed')
def assert_number_of_queries_executed(step, query_count):
    queries = step.scenario.number_of_queries
    message = "Queries Executed: %s, Max Queries Expected %s" % (queries, query_count)
    assert queries == int(query_count), message


