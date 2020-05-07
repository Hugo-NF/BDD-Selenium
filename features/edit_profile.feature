# encoding: utf-8

Feature: Edit Profile
  As a logged in user
  I want to change information belonging my profile

  Scenario: Change data with correct password
    Factory: As An Authenticated User
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/a/div/div/span"
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/div/a[1]"
    Then I should be redirected to "/Auth/EditProfile" page
    When I fill the form with
      |DisplayName|Hugo "BDD" Fonseca|
      |phoneInput|(61)99999-8888     |
      |CurrentPassword|123456789|
    And I submit form
    Then I should see one "alert" with "Perfil modificado com sucesso"

  Scenario: Change data with incorrect password
    Factory: As An Authenticated User
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/a/div/div/span"
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/div/a[1]"
    Then I should be redirected to "/Auth/EditProfile" page
    When I fill the form with
      |DisplayName|Hugo "BDD" Fonseca|
      |phoneInput|(61)99999-8888     |
      |CurrentPassword|1234567890|
    And I submit form
    Then I should see one "alert" with "Senha atual incorreta"


  Scenario: Change password
    Factory: As An Authenticated User
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/a/div/div/span"
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/div/a[1]"
    Then I should be redirected to "/Auth/EditProfile" page
    When I fill the form with
      |Password|1234567899|
      |ConfirmPassword|1234567899|
      |CurrentPassword|123456789|
    And I submit form
    Then I should see one "alert" with "Perfil modificado com sucesso"
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/a/div/div/span"
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/div/a[1]"
    Then I should be redirected to "/Auth/EditProfile" page
    When I fill the form with
      |Password|123456789|
      |ConfirmPassword|123456789|
      |CurrentPassword|1234567899|
    And I submit form
    Then I should see one "alert" with "Perfil modificado com sucesso"