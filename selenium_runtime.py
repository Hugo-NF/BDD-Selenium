import logging

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options

from definitions import *


class SeleniumRuntime:

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

    def current_url(self):
        return self.browser.current_url


selenium_runtime = SeleniumRuntime()
