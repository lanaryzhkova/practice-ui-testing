from pages.base_page import BasePage, Element
from selenium.webdriver.common.by import By

class ProductPage(BasePage):
    product_quantity = Element((By.ID, "product_quantity"))
    add_to_cart_button = Element((By.CSS_SELECTOR, ".productpagecart"))

    def set_product_quantity(self, quantity):
        self.send_keys(self.product_quantity, str(quantity))
        return self
    
    def add_product_to_cart(self):
        self.click(self.add_to_cart_button)
        return self