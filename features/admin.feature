# encoding: utf-8

Feature: Admin
  As a logged in administrator
  I want to access administrative features

  Scenario: Access Log
    Factory: As An Authenticated User
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/a/div/div/span"
    And I click on "xpath" with "/html/body/div[2]/nav/div[2]/div/ul[3]/li/div/a[5]"
    Then I should be redirected to "/ActivityLog/Log" page