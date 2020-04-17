class When:
    @staticmethod
    def i_fill_the_form_with(table):
        print("Running: When I Fill the form with %s" % table)
        pass


class And:
    @staticmethod
    def i_click_on_button(button):
        print("Running: And I Click On Button %s" % button)
        pass


class Given:
    @staticmethod
    def that_i_am_at_page(login):
        print("Running: Given That I Am At Page %s" % login)
        pass


class Then:
    @staticmethod
    def i_should_be_redirected_to_page(dashboard):
        print("Running: Then I Should Be Redirected To Page %s" % dashboard)
        pass
