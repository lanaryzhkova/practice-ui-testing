from pages.base_page import BasePage, Element
from selenium.webdriver.common.by import By
from data.data import BASE_URL
from utils import utils

class MainPage(BasePage):
    category_links = (By.XPATH, "//*[@id='categorymenu']/nav/ul/li/a")
    sorting_select = Element((By.ID, "sort"))
    option_name_az = Element((By.CSS_SELECTOR, "#sort > option[value='pd.name-ASC']"))
    option_name_za = Element((By.CSS_SELECTOR, "#sort > option[value='pd.name-DESC']"))
    option_price_low_high = Element((By.CSS_SELECTOR, "#sort > option[value='p.price-ASC']"))
    option_price_high_low = Element((By.CSS_SELECTOR, "#sort > option[value='p.price-DESC']"))
    grid_products_in_category = ((By.CSS_SELECTOR, "#maincontainer .thumbnails.grid.row.list-inline"))
    grid_products_in_home = (By.CSS_SELECTOR, "#maincontainer .thumbnails.list-inline")
    button_add_to_cart = (By.CSS_SELECTOR, ".productcart")
    name_product = (By.XPATH, "//a[@class='prdocutname']")
    card_product = (By.CSS_SELECTOR, "[class*='thumbnail']")
    value_price = value_price = (By.CSS_SELECTOR, ".oneprice, .pricenew")
    
    def load(self):
        self.open(BASE_URL)
        self.driver.get(BASE_URL)
        self.wait.wait_for_url(BASE_URL)
        return self
    
    def click_category(self, category_name):
        categories = self.find_elements(self.category_links)
        for category in categories:
            if category_name in category.text:
                self.click(category)
                return self
        raise ValueError(f"Категория '{category_name}' не найдена")
    
    def click_product_by_position_in_category(self, position):
        grid_products = self.find_element(self.grid_products_in_category)
        products = grid_products.find_elements(*self.name_product)
        if position < 1 or position > len(products):
            raise ValueError(f"Позиция {position} вне диапазона доступных товаров")
        self.click(products[position - 1])
        return self
    
    def click_product_by_position_in_home(self, position):
        products = [p for p in self.find_elements(self.name_product) if p.is_displayed()]
        if position < 0 or position >= len(products):
            raise ValueError(f"Позиция {position} вне диапазона доступных товаров")
        self.click(products[position])
        return self
    
    def select_sorting_option(self, option_text):
        self.click(self.sorting_select)
        options = [
            self.option_name_az,
            self.option_name_za,
            self.option_price_low_high,
            self.option_price_high_low
        ]
        for option in options:
            if option.text.strip() == option_text:
                self.click(option)
                return self
        raise ValueError(f"Опция сортировки '{option_text}' не найдена")
    
    def get_product_names_in_category(self):
        grid_products = self.find_element(self.grid_products_in_category)
        products = [p for p in grid_products.find_elements(*self.name_product) if p.is_displayed()]
        names = []
        for product in products:
            names.append(product.text.strip())
        return names
    
    def get_product_names_in_home(self):
        products = self.find_elements(self.name_product)
        names = []
        for product in products:
            names.append(product.text.strip())
        return names
    
    def get_product_prices(self):
        grid_products = self.find_element(self.grid_products_in_category)
        products = grid_products.find_elements(*self.value_price)
        prices = []
        for product in products:
            prices.append(product.text.strip())
        return utils.prices_array_handle(prices)

    