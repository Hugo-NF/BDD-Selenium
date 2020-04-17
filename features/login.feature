# encoding: utf-8

Feature: Login
  As a previous registered user
  I want to sign in and sign out the application

  Scenario: Correct Password
    Given that I am at "login" page
    When I fill the form with
      |Email|hugo.fonseca@grupoorion.eng.br|
      |Password|123456|
    And I click on "Entrar" button
    Then I should be redirected to "Dashboard" page

Feature: Register
  As a not registered user
  I want to register on platform

  Scenario: Correct Email
    Given that I am at "register" page
    When I fill the form with
      |Email|hugo.fonseca@grupoorion.eng.br|
      |Password|123456|
    And I click on "Registrar" button
    Then I should be redirected to "Home" page
