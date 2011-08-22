Feature: ForeignKeyChoiceField

    Scenario: Django's default queries each form for foreign key values
        Given a page with "10" people forms
        When I visit the "many_queries" page
        Then I expect there to be "11" queries executed

    Scenario: Does not query related models for each form in formset
        Given a page with "10" people forms
        When I visit the "few_queries" page
        Then I expect there to be "2" queries executed

