Feature: QuerysetChoiceField

    Scenario: Build a select with a queryset and save only the pk
        Given the eye colors
        | name |
        | blue |
        | red  |
        And a web browser
        When I visit the "querysetchoice" page
        And post the form with
        | name | eye_color | second_eye_color |
        | alex | 1         | 2                |
        Then I expect a person with the name of "alex" to have a second_eye_color of "2"
        And an eye_color of the EyeColor model instance for pk "1"
