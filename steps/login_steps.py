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


class Given:
    @staticmethod
    def that_i_am_at_page(login):
        browser.go_to_page("http://orionconnect.azurewebsites.net/Auth/" + login)


class Then:
    @staticmethod
    def i_should_be_redirected_to_page(dashboard):
        sleep(10)  # Waiting for redirect
        assert browser.current_url() == "http://orionconnect.azurewebsites.net/" + dashboard
