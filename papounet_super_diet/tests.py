"""
    This is were the user stories are to be tested !

    Are tested:
        The User story where the persona wants to look for a product
                without logging in.
        A full story from login to the record of a product.

    To be noticed:
        By removing the carret at last line, the current html code
            will be displayed: very convenient for debugging.

"""
from django.test import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Firefox


class CustomerTestCase(LiveServerTestCase):
    fixtures = ['product', 'store', 'user']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = Firefox()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_quickly_get_product_from_home_page(self):
        """
            Test the User story where the persona wants to look for a product
            without logging in.
            By removing the carret at last line, the current html code
            will be displayed: very convenient for debugging.
        """
        self.browser.get('%s%s' % (self.live_server_url, ''))
        self.browser.find_element_by_id("favicon")
        # First of all, Lily Kala has a look at the page
        # At the top, she can see a navigation bar displaying:
        # The company logo
        self.browser.find_element_by_id("company_logo")
        # The company name
        self.browser.find_element_by_css_selector("img#company_logo")
        # The possibility to log in
        self.browser.find_element_by_id("login")
        customer_input = self.browser.find_element_by_name(
            'searched_item')
        self.assertEqual(customer_input.get_attribute(
            'placeholder'), 'Votre Recherche')
        # In the upper half of the page, a picture
        self.browser.find_element_by_css_selector('img#background_picture')
        # Contains the motto and a piece of advice
        self.browser.find_element_by_css_selector('h2#motto')
        self.browser.find_element_by_css_selector('h3#advice')
        # and a search field with a validation button (see below)
        # Just below Lily Kala can see the story of the company
        self.browser.find_element_by_css_selector('h3#heroes')
        self.browser.find_element_by_css_selector('h4#story')
        # With the pictures of Colette and Remy
        self.browser.find_element_by_css_selector('img#Colette')
        self.browser.find_element_by_css_selector('img#Remy')
        # Still below LK sees an invite to contact the company
        self.browser.find_element_by_css_selector('h4#call_to_action')
        # Per telephone
        self.browser.find_element_by_css_selector('img#telephone')
        self.browser.find_element_by_css_selector('p#phone_number')
        # Or per e-mail
        self.browser.find_element_by_css_selector(
            'img#e_mail')
        self.browser.find_element_by_css_selector('p#e_mail')
        # At the bottom of the page, she can find the terms of reference
        self.browser.find_element_by_css_selector('a#terms_of_use')
        # Then she enters the name of a certain product
        # in a dedicated input box either at the top and validate
        customer_input.send_keys('No Product')
        # Or in the middle of the page
        # Then she validates
        self.browser.find_element_by_id('top_button').click()
        # A new window opens
        # LK is informed that no product was found
        self.browser.find_element_by_tag_name('h2')
        # The input field is initialized
        # LK is invited to input another product name
        customer_input = self.browser.find_element_by_name(
            'searched_item')
        customer_input.clear()
        customer_input.send_keys('Nutella')
        # And she can validate the search
        self.browser.find_element_by_id('top_button').click()
        # Then a list of max 6 comparable products
        elements = self.browser.find_elements_by_class_name("img-in-card")
        assert len(elements) > 0
        # with an equivalent or better nutrition grade is displayed
        # The name of the product can be seen below the picture
        self.browser.find_element_by_id("01234567891011")
        # LK selects a product to get some details
        self.browser.find_element_by_id("01234567891011").click()
        # A new window opens, showing the details
        WebDriverWait(self.browser, 2)
        self.browser.find_element_by_class_name('card-deck')
        self.browser.find_element_by_class_name('list-group')
        # print(self.browser.page_source)

    def test_log_in_then_search_for_product_and_record_it(self):
        """
            Test a full story from login to the record of a product.
            By removing the carret at last line, the current html code
            will be displayed: very convenient for debugging.
        """
        self.browser.get('%s%s' % (self.live_server_url, ''))
        # As a registered member/customer LK clicks on login icon
        self.browser.find_element_by_id("login").click()
        # The login page is displayed
        self.browser.find_element_by_class_name("login-form")
        # LK inputs her username
        customer_input = self.browser.find_element_by_id('id_username')
        customer_input.clear()
        customer_input.send_keys('user')
        # and her password
        customer_input = self.browser.find_element_by_id('id_password')
        customer_input.clear()
        customer_input.send_keys('testuser01')
        self.browser.find_element_by_id('submit-login').click()
        # The icon "logout" is diplayed
        WebDriverWait(self.browser, 2)
        self.browser.find_element_by_id('logout')
        # The icon to access the favorites as well
        self.browser.find_element_by_id('carrot')
        customer_input = self.browser.find_element_by_name(
            'searched_item')
        customer_input.clear()
        customer_input.send_keys('Nutella')
        # And she can validate the search
        self.browser.find_element_by_id('top_button').click()
        # Then a list of max 6 comparable products
        self.browser.find_elements_by_class_name("card-img-top")
        # LK saves a product
        self.browser.find_element_by_id(
            'record-product-01234567891011').click()
        # Then LK checks the favorites by clicking on a carrot logo
        self.browser.find_element_by_id('carrot').click()
        # She wants the details of a product and clicks on it
        self.browser.find_element_by_id("01234567891011").click()
        # Then she sees the details of the product
        # And closes the window to get back to her favorites
        self.browser.find_element_by_id("back_to_favorites").click()
        self.browser.find_element_by_class_name("img-in-card")
        # print(self.browser.page_source)
