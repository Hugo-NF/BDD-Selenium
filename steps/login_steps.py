from selenium_runtime import selenium_runtime as browser
from time import sleep


class Given:
    @staticmethod
    def that_i_am_at_page(login):
        browser.go_to_page(login)


class Then:
    @staticmethod
    def i_should_be_redirected_to_page(dashboard):
        sleep(10)  # Waiting for redirect
        assert browser.current_url() == dashboard
