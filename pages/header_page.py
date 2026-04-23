from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure

class HeaderPage(BasePage):
    search_input = (By.ID, "filter_keyword")
    search_button = (By.CSS_SELECTOR, ".button-in-search")

    @allure.step("Поиск товара '{product_name}'")
    def search_for_product(self, product_name: str) -> 'HeaderPage':
        """Вводит название товара в строку поиска и нажимает кнопку поиска"""
        self.send_keys_to_input(self.search_input, product_name)
        self.click(self.search_button)
        return self
    
    def check_header_visible(self):
        return self.find_element(self.search_input)