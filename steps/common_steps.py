from selenium_runtime import selenium_runtime as browser
from selenium.webdriver.common.by import By
from time import sleep

base_url = "https://orionconnect.azurewebsites.net"


class Given:
    @staticmethod
    def that_i_am_at_page(login):
        browser.go_to_page(base_url + login)


class Then:
    @staticmethod
    def i_should_be_redirected_to_page(dashboard):
        assert browser.wait_for_redirect(base_url + dashboard)

    @staticmethod
    def i_should_see_one_with(class_name, text):
        element = browser.wait_for_element(class_name, By.CLASS_NAME)
        assert text in element.text


class When:
    @staticmethod
    def i_fill_the_form_with(table):
        browser.fill_form(table)

    @staticmethod
    def i_fill_selects_with(table):
        sleep(5)
        browser.fill_selects(table)


class And:
    @staticmethod
    def i_click_on_with(selector, value):
        if selector == 'xpath':
            element = browser.wait_for_element(value, By.XPATH)
            element.click()
        if selector == 'id':
            element = browser.wait_for_element(value, By.ID)
            element.click()

    @staticmethod
    def i_submit_form():
        browser.submit_form()
