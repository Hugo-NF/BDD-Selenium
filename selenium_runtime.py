import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

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
            element.clear()
            element.send_keys(value)

    def fill_selects(self, table):
        for field_name, field_value in table.items():
            self.wait_for_element(field_value, By.XPATH).click()

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

    def wait_for_element(self, value, by=By.ID, timeout=30):
        return WebDriverWait(self.browser, timeout).until(
            expected_conditions.presence_of_element_located((by, value))
        )

    def wait_for_redirect(self, target_url, timeout=30):
        return WebDriverWait(self.browser, timeout).until(
            expected_conditions.url_to_be(target_url)
        )

    @staticmethod
    def assert_class(element, class_name):
        class_attr = element.get_attribute('class')
        return class_attr.find(class_name) >= 0

    @staticmethod
    def assert_attribute(element, attribute_name, attribute_value):
        attr_value = element.get_attribute(attribute_name)
        return attr_value.find(attribute_value) >= 0


selenium_runtime = SeleniumRuntime()
