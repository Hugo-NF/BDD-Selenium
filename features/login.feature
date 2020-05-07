# encoding: utf-8

Feature: Login
  As a previous registered user
  I want to sign in and sign out the application

  Scenario: Correct Password
    Given that I am at "/Auth/Login" page
    When I fill the form with
      |Email|hugo.fonseca@grupoorion.eng.br|
      |Password|123456789|
    And I submit form
    Then I should be redirected to "/Dashboard" page

  Scenario: Wrong Password or Inexistent Account
    Given that I am at "/Auth/Login" page
    When I fill the form with
      |Email|hugo.fonseca@grupoorion.eng.br|
      |Password|123456                     |
    And I submit form
    Then I should see one "alert" with "Credenciais inválidas"

  Scenario: Pending Activation
    Given that I am at "/Auth/Login" page
    When I fill the form with
      |Email|hugonfonseca@hotmail.com|
      |Password|123456               |
    And I submit form
    Then I should see one "alert" with "Sua conta ainda não foi ativada!"
