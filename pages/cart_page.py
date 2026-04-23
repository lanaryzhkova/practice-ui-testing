import os
import logging

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from data.data import CART_URL
from pages.base_page import BasePage
from utils.utils import price_str_handle

py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

worker_id = os.getenv("PYTEST_XDIST_WORKER", "main")

if not py_logger.handlers:
    py_handler = logging.FileHandler(f"{__name__}_{worker_id}.log", mode='a')
    py_formatter = logging.Formatter(
        "%(name)s %(asctime)s %(levelname)s %(message)s"
    )
    py_handler.setFormatter(py_formatter)
    py_logger.addHandler(py_handler)


class CartPage(BasePage):
    products_list = (By.XPATH, "//*[@id='cart']/div/div[1]/table")
    product_row = (By.XPATH, "./tbody/tr")
    product_quantity = (By.XPATH, ".//td[5]//input")
    product_unit_price = (By.XPATH, "./td")
    product_total_price = (By.XPATH, "./td")
    update_cart_button = (By.ID, "cart_update")
    total_amount_value = (By.XPATH,
                          "//*[@id='totals_table']/tbody/tr[3]/td[2]/span")
    totals_table = (By.ID, "totals_table")
    flat_shipping_rate = (By.XPATH,
                          "//*[@id='totals_table']/tbody/tr[2]/td[2]/span")
    remove_product_button = (By.XPATH, ".//a[contains(@href, 'remove')]")
    product_name = (By.CSS_SELECTOR, "[class*='align_left']")

    @allure.step("Загрузка страницы корзины")
    def open_cart_page(self) -> 'CartPage':
        """Открывает страницу корзины и ожидает загрузки URL"""
        self.open(CART_URL)
        self.wait.wait_for_element_visible(self.products_list)
        py_logger.info(f"Загружена страница {CART_URL}")
        return self

    @allure.step("Получение списка всех продуктов в корзине")
    def get_all_products_in_cart(self) -> list[WebElement]:
        """Возвращает список всех продуктов в корзине"""
        products_list = self.find_element(self.products_list)
        products = products_list.find_elements(*self.product_row)
        return products[1:]

    def cheapest_product_on_cart(self) -> WebElement:
        """Поиск самого дешёвого товара в корзине"""
        products = self.get_all_products_in_cart()

        cheapest_product = products[0]
        cheapest_price = float(
            self.get_product_unit_price_in_cart(products[0]))

        for product in products[1:]:
            price = float(self.get_product_unit_price_in_cart(product))

            if price < cheapest_price:
                cheapest_price = price
                cheapest_product = product
        name = self.get_product_name_in_cart(cheapest_product)
        py_logger.info(f"Найден самый дешёвый товар {name}(${cheapest_price})")
        return cheapest_product

    def get_product_quantity_in_cart(self, product: WebElement) -> int:
        """Получает количество конкретного товара в корзине"""
        quantity_element = product.find_element(*self.product_quantity)
        value = self.get_attribute_of_element(quantity_element, "value")
        return int(float(value)) if value else 0

    def get_product_unit_price_in_cart(self, product: WebElement) -> float:
        """Получает цену за единицу конкретного товара в корзине"""
        price_element = product.find_elements(*self.product_unit_price)[3]
        price = price_str_handle(price_element)
        return float(price) if price else 0.0

    def get_product_name_in_cart(self, product: WebElement) -> str:
        """Получает название конкретного товара в корзине"""
        name_element = product.find_elements(
            *self.product_name)[0]
        return self.text_of(name_element)

    def change_product_quantity(self, quantity, product):
        """Изменяет количество конкретного товара в корзине"""
        quantity_element = product.find_element(*self.product_quantity)
        self.send_keys_to_input(quantity_element, str(quantity))
        name = self.get_product_name_in_cart(product)
        py_logger.info(f"Изменено количество товара {name} на {quantity}")
        return self

    def click_update_cart(self) -> 'CartPage':
        """Нажимает кнопку обновления корзины"""
        self.click(self.find_element(self.update_cart_button))
        return self

    def get_cart_total(self) -> float:
        """Получает общую сумму корзины из элемента на странице"""
        return price_str_handle(self.find_element(self.total_amount_value))

    def get_shipping_cost(self) -> float:
        """Получает стоимость доставки из элемента на странице"""
        return price_str_handle(self.find_element(self.flat_shipping_rate))

    def get_products_count_in_cart(self) -> int:
        """Получает количество товаров, добавленных в корзину"""
        products = self.get_all_products_in_cart()
        return len(products)

    def calculating_total_price(self) -> float:
        """Вычисляет общую сумму корзины на основе количества и цены товара"""
        products = self.get_all_products_in_cart()
        total = 0.0
        for product in products:
            quantity = self.get_product_quantity_in_cart(product)
            price = self.get_product_unit_price_in_cart(product)
            try:
                total += quantity * price
            except ValueError:
                continue
        return total + self.get_shipping_cost()

    def get_product_by_position_in_cart(self, position: int) -> WebElement:
        """Получает элемент товара в корзине по его позиции (начиная с 1)"""
        products = self.get_all_products_in_cart()
        if 1 <= position < len(products):
            return products[position]
        raise IndexError("Неверная позиция продукта в корзине")

    def remove_product_from_cart(self, product: WebElement) -> None:
        """Удаляет конкретный товар из корзины"""
        remove_button = product.find_element(*self.remove_product_button)
        self.click(remove_button)

    @allure.step("Удаление чётных продуктов из корзины")
    def remove_even_products_from_cart(self) -> None:
        """Удаляет товары на четных позициях в корзине (начиная с 1)"""
        products = self.get_all_products_in_cart()
        py_logger.info(f"Сейчас в корзине товары: {products}")
        products_count = len(products)

        for position in range(products_count, 0, -1):
            if position % 2 == 0:
                products = self.get_all_products_in_cart()
                product = products[position - 1]
                product_name = self.get_product_name_in_cart(product)
                remove_button = product.find_element(
                    *self.remove_product_button)
                self.click(remove_button)
                py_logger.info(f"Удалён продукт {product_name}")

    @allure.step("Получение списка всех названий продуктов в корзине")
    def get_all_products_names_in_cart(self) -> list:
        """Получение списка всех названий продуктов в корзине"""
        products = self.get_all_products_in_cart()
        product_names = []
        for product in products:
            product_name = self.get_product_name_in_cart(product)
            product_names.append(product_name)
        return product_names

    @allure.step("Проверка наличия продукта по имени в корзине")
    def check_product_by_name(self, product_name: str) -> bool:
        """Проверка наличия продукта по имени в корзине"""
        products = self.get_all_products_in_cart()
        for product in products:
            name = self.get_product_name_in_cart(product).lower()
            if product_name in name:
                py_logger.info(f"Продукт {name} успешно добавлен в корзину")
                return True
        py_logger.warning(f"Продукт {name} не удалось добавить в корзину")
        return False

    @allure.step("Получение рассчитанной и фактической суммы корзины")
    def get_cart_totals(self) -> tuple[float, float]:
        """Получение рассчитанной и фактической суммы корзины"""
        calculated_total = self.calculating_total_price()
        py_logger.info(f"Ожидаемая итоговая сумма: {calculated_total} ")
        cart_total = self.get_cart_total()
        py_logger.info(f"Фактическая итоговая сумма: {cart_total} ")
        return calculated_total, cart_total

    @allure.step("Увеличение в 2 раза количества самого дешевого товара")
    def increase_cheapest_product_quantity(self) -> 'CartPage':
        """Увеличение в 2 раза количества самого дешевого товара в корзине"""
        cheapest_product = self.cheapest_product_on_cart()
        current_quantity = self.get_product_quantity_in_cart(cheapest_product)
        name = self.get_product_name_in_cart(cheapest_product)
        py_logger.info(f"Текущее количество товара {name}")
        new_quantity = current_quantity * 2
        self.change_product_quantity(new_quantity, cheapest_product)
        self.find_element(self.update_cart_button)
        self.click_update_cart()
        return self
