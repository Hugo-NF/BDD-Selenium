# encoding: utf-8

Feature: Login
  As a previous registered user
  I want to sign in and sign out the application

  Scenario: Correct Password
    Given that I am at "login" page
    When I fill the form with:
      |Email|hugo.fonseca@grupoorion.eng.br|
      |Password|123456|
    And I click on "Entrar" button
    Then I should be redirected to "Dashboard" page