Feature: SDS Website Functionalities

  Scenario: View customer count
    Given I am on the SDS homepage
    Then I should see how many customers SDS have

  Scenario: View user count
    Given I am on the SDS homepage
    Then I should see how many users SDS have

  Scenario: Request a Landval demo
    Given I am a potential customer of SDS
    When I fill in the demo request form with valid data
    Then the form should be submitted successfully
