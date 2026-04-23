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

class HeaderPage(BasePage):
    """Класс, описывающий заголовок страницы"""
    search_input = (By.ID, "filter_keyword")
    search_button = (By.CSS_SELECTOR, ".button-in-search")

    @allure.step("Поиск товара '{product_name}'")
    def search_for_product(self, product_name: str) -> 'HeaderPage':
        """Вводит название товара в строку поиска и нажимает кнопку поиска"""
        self.send_keys_to_input(self.search_input, product_name)
        self.click(self.find_element(self.search_button))
        py_logger.info(f"Поиск {product_name}")
        return self

    def check_header_visible(self):
        """Проверяет отображение поисковой строки"""
        return self.find_element(self.search_input)
