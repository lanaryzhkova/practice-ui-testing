import allure
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")

py_handler.setFormatter(py_formatter)

py_logger.addHandler(py_handler)

class ProductPage(BasePage):
    """Класс, описывающий страницу товара"""
    product_quantity = (By.ID, "product_quantity")
    add_to_cart_button = (By.CSS_SELECTOR, ".productpagecart")

    @allure.step("Выбор количества товара {quantity} на странице продукта")
    def set_product_quantity_in_product_page(self,
                                             quantity: int) -> 'ProductPage':
        """Устанавливает количество товара на странице продукта"""
        self.send_keys_to_input(self.product_quantity, str(quantity))
        return self

    @allure.step("Добавление товара в корзину")
    def add_product_to_cart(self) -> 'ProductPage':
        """Кликает на кнопку 'Add to Cart' на странице продукта"""
        self.click(self.find_element(self.add_to_cart_button))
        return self
