from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from data.data import BASE_URL
from utils import utils
import allure
import logging

py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)


py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

py_handler.setFormatter(py_formatter)

py_logger.addHandler(py_handler)

class MainPage(BasePage):
    category_links = (By.XPATH, "//*[@id='categorymenu']/nav/ul/li/a")
    sorting_select = (By.ID, "sort")
    option_name_az = (By.CSS_SELECTOR, "#sort > option[value='pd.name-ASC']")
    option_name_za = (By.CSS_SELECTOR, "#sort > option[value='pd.name-DESC']")
    option_price_low_high = (By.CSS_SELECTOR, "#sort > option[value='p.price-ASC']")
    option_price_high_low = (By.CSS_SELECTOR, "#sort > option[value='p.price-DESC']")
    grid_products_in_category = (By.CSS_SELECTOR, "#maincontainer .thumbnails.grid.row.list-inline") 
    grid_products_in_home = (By.CSS_SELECTOR, "#maincontainer .thumbnails.list-inline")
    button_add_to_cart = (By.CSS_SELECTOR, ".productcart")
    name_product = (By.XPATH, "//a[@class='prdocutname']")
    card_product = (By.CSS_SELECTOR, "[class*='thumbnail']")
    value_price = value_price = (By.CSS_SELECTOR, ".oneprice, .pricenew")
    
    @allure.step("Загрузка главной страницы")
    def open_main_page(self) -> 'MainPage':
        """Открывает главную страницу и ожидает загрузки URL"""
        self.open(BASE_URL)
        self.wait.wait_for_url(BASE_URL)
        return self
    
    @allure.step("Выбор категории {category_name}")
    def click_category(self, category_name: str) -> 'MainPage':
        """Находит категорию по названию и кликает на неё"""
        categories = self.find_elements(self.category_links)
        for category in categories:
            if category_name in category.text:
                self.click(category)
                return self
        raise ValueError(f"Категория '{category_name}' не найдена")
    
    @allure.step("Выбор товара по позиции {position} в категории")
    def click_product_by_position_in_category(self, position: int) -> 'MainPage':
        """Кликает на товар по его позиции (на странице категории,начиная с 1)"""
        grid_products = self.find_element(self.grid_products_in_category)
        products = grid_products.find_elements(*self.name_product)
        if position < 1 or position > len(products):
            raise ValueError(f"Позиция {position} вне диапазона доступных товаров")
        self.click(products[position - 1])
        return self
    
    def click_product_by_position_in_home(self, position: int) -> 'MainPage':
        """Кликает на товар по его позиции (на главной странице, начиная с 1)"""
        products = [p for p in self.find_elements(self.name_product) if p.is_displayed()]
        if position < 0 or position >= len(products):
            raise ValueError(f"Позиция {position} вне диапазона доступных товаров")
        self.click(products[position])
        return self
    
    @allure.step("Сортировка по {option_text}")
    def select_sorting_option(self, option_text: str) -> 'MainPage':
        """Выбирает опцию сортировки по её тексту"""
        self.click(self.sorting_select)
        options = [
            self.option_name_az,
            self.option_name_za,
            self.option_price_low_high,
            self.option_price_high_low
        ]
        for option in options:
            if self.get_text(option) == option_text:
                self.click(option)
                return self
        raise ValueError(f"Опция сортировки '{option_text}' не найдена")
    
    def get_product_names_in_category(self) -> list[str]:
        """Возвращает список названий товаров, отображаемых на странице категории"""
        grid_products = self.find_element(self.grid_products_in_category)
        products = [p for p in grid_products.find_elements(*self.name_product) if p.is_displayed()]
        names = []
        for product in products:
            names.append(self.get_text(product))
        return names
    
    def get_product_names_in_home(self) -> list[str]:
        """Возвращает список названий товаров, отображаемых на главной странице"""
        products = self.find_elements(self.name_product)
        names = []
        for product in products:
            names.append(self.get_text(product))
        return names
    
    def get_product_prices_in_category(self) -> list[float]:
        """Возвращает список цен товаров, отображаемых на странице категории"""
        grid_products = self.find_element(self.grid_products_in_category)
        products = grid_products.find_elements(*self.value_price)
        prices = []
        for product in products:
            prices.append(self.get_text(product))
        return utils.prices_array_handle(prices)

    