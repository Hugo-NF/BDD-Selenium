from selenium_runtime import selenium_runtime as browser
from selenium.webdriver.common.by import By
from time import sleep


class And:
    @staticmethod
    def i_click_on_with(selector, value):
        sleep(5)  # Loader animation
        if selector == 'xpath':
            element = browser.wait_for_element(value, By.XPATH)
            element.click()
        elif selector == 'text':
            element = browser.wait_for_element(value, By.PARTIAL_LINK_TEXT)
            element.click()
