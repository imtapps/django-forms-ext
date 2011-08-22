Feature: Simple Generic Formset View

    Scenario: The formset view passes a formset into the template context
        Given a web browser
        When I visit the "simple" page
        Then I expect to have "formset" in the template context

