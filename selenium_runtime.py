import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import invisibility_of_element
from selenium.webdriver.support.wait import WebDriverWait

# Supported browsers
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver import Edge

from definitions import *


class SeleniumRuntime:
    """
    This class works like a singleton containing a single instance of the browser environment

    Attributes:
        logger: logger instance gathered from logging module, acts like a singleton
    """

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_INSTANCE)

        if TARGET_BROWSER == 'chrome':
            self.browser = Chrome()
        elif TARGET_BROWSER == 'firefox':
            self.browser = Firefox()
        elif TARGET_BROWSER == 'edge':
            self.browser = Edge()

    def go_to_page(self, url):
        self.browser.get(url)

    def submit_form(self):
        form = self.browser.find_element_by_tag_name('form')
        form.submit()

    def fill_form(self, table):
        for field, value in table.items():
            element = self.browser.find_element_by_id(field)
            element.send_keys(value)

    def click(self, value, by=By.ID):
        element = self.browser.find_element(by, value)
        element.click()

    def get_element(self, value, by=By.ID):
        return self.browser.find_element(by, value)

    def get_elements(self, value, by=By.ID):
        return self.browser.find_elements(by, value)

    def assert_presence(self, value, by=By.ID):
        try:
            self.browser.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def back(self):
        self.browser.back()

    def forward(self):
        self.browser.forward()

    def refresh(self):
        self.browser.refresh()

    def current_title(self):
        return self.browser.title

    def current_url(self):
        return self.browser.current_url

    def wait_for_loader(self, timeout=30):
        WebDriverWait(self.browser, timeout).until(invisibility_of_element('.loader'))

    @staticmethod
    def assert_class(element, class_name):
        class_attr = element.get_attribute('class')
        return class_attr.find(class_name) >= 0

    @staticmethod
    def assert_attribute(element, attribute_name, attribute_value):
        attr_value = element.get_attribute(attribute_name)
        return attr_value.find(attribute_value) >= 0


selenium_runtime = SeleniumRuntime()
