from pages.base_page import BasePage, Element
from selenium.webdriver.common.by import By

class HeaderPage(BasePage):
    search_input = Element((By.ID, "filter_keyword"))
    search_button = Element((By.CSS_SELECTOR, ".button-in-search"))

    def search_for_product(self, product_name):
        self.send_keys(self.search_input, product_name)
        self.click(self.search_button)
        return self
