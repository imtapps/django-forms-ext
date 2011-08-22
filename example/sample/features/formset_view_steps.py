from lettuce import step, world, before

@step(u'Given the "(.*)" page')
def given_a_page(step, page_name):
    world.page_name = page_name

@step(u'Then I expect to have "(.*)" in the template context')
def then_i_expect_to_have_group1_in_the_template_context(step, variable_name):
    assert variable_name in world.response.context, "%s not in template context" % variable_name
