from selenium_runtime import selenium_runtime as browser
from steps.common_steps import base_url


class AsAnAuthenticatedUser:

    @staticmethod
    def run():
        browser.go_to_page(base_url + "/Auth/Login")
        browser.fill_form({"Email": "hugo.fonseca@grupoorion.eng.br", "Password": "123456789"})
        browser.submit_form()
        pass
