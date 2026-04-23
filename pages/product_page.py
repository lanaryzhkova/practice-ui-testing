from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure

class ProductPage(BasePage):
    product_quantity = (By.ID, "product_quantity")
    add_to_cart_button = (By.CSS_SELECTOR, ".productpagecart")

    @allure.step("Выбор количества товара {quantity} на странице продукта")
    def set_product_quantity_in_product_page(self, quantity: int) -> 'ProductPage':
        """Устанавливает количество товара на странице продукта"""
        self.send_keys_to_input(self.product_quantity, str(quantity))
        return self
    
    @allure.step("Добавление товара в корзину")
    def add_product_to_cart(self) -> 'ProductPage':
        """Кликает на кнопку 'Add to Cart' на странице продукта"""
        self.click(self.add_to_cart_button)
        return self