# encoding: utf-8

Feature: Navigation
  As a logged in administrator
  I want to access navigate across the features

  Scenario: Access Log
    Factory: As An Authenticated User
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/a/div/div/span"
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/div/a[5]"
    Then I should be redirected to "/ActivityLog/Log" page

  Scenario: Access Location
    Factory: As An Authenticated User
    And I click on "text" with "Localização"
    Then I should be redirected to "/Localizacao" page

  Scenario: Change building
    Factory: As An Authenticated User
    And I click on "text" with "Trocar edifício"
    Then I should be redirected to "/" page
    When I fill selects with
      |enterpriseSelect|ORION TELECOMUNICAÇÕES ENGENHARIA S/A|
      |buildingSelect|Escritório - SP|
    And I click on "text" with "Alterar"
    Then I should be redirected to "/Dashboard" page
    Then I should see one "list-group-item" with "Escritório-SP"