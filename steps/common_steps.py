from selenium_runtime import selenium_runtime as browser
from time import sleep


class When:
    @staticmethod
    def i_fill_the_form_with(table):
        browser.fill_form(table)


class And:
    @staticmethod
    def i_submit_form():
        browser.submit_form()
