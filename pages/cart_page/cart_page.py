from data.data import CART_URL
from pages.base_page import BasePage, Element
from selenium.webdriver.common.by import By

from utils.utils import price_str_handle

class CartPage(BasePage):
    products_list = ((By.XPATH, "//*[@id='cart']/div/div[1]/table"))
    product_row = ((By.XPATH, "./tbody/tr"))
    product_quantity = ((By.XPATH, ".//td[5]//input"))
    product_unit_price = ((By.XPATH, "./td")) 
    product_total_price = ((By.XPATH, "./td")) 
    update_cart_button = Element((By.ID, "cart_update"))
    total_amount_value = Element((By.XPATH, "//*[@id='totals_table']/tbody/tr[3]/td[2]/span"))
    totals_table = Element((By.ID, "totals_table"))
    flat_shipping_rate = Element((By.XPATH, "//*[@id='totals_table']/tbody/tr[2]/td[2]/span")) 
    remove_product_button = (By.XPATH, ".//a[contains(@href, 'remove')]")
    product_name = (By.CSS_SELECTOR, "[class*='align_left']")

    def load(self):
        self.open(CART_URL)
        return self
    
    def get_all_products_in_cart(self):
        products_list = self.find_element(self.products_list)
        products = products_list.find_elements(*self.product_row)
        products_names = []
        for product in products[1:]:
            name = self.get_product_name(product)
            products_names.append(name)
        return products[1:]

    def cheapest_product(self):
        products = self.get_all_products_in_cart()
        cheapest = None
        for product in products:
            price_text = self.get_product_unit_price(product)
            try:
                price = float(price_text)
                if cheapest is None or price < cheapest[1]:
                    cheapest = (product, price)
            except ValueError:
                continue
        return cheapest[0] if cheapest else None

    def get_product_quantity(self, product):
        quantity_element = product.find_element(*self.product_quantity)
        return int(quantity_element.get_attribute("value"))
    
    def get_product_unit_price(self, product):
        price_element = product.find_elements(*self.product_unit_price)[3]
        price = price_str_handle(price_element)
        return price
    
    def get_product_name(self, product):
        name_element = product.find_elements(*self.product_name)[0]
        return name_element.text.strip()
    
    def change_product_quantity(self, quantity, product):
        quantity_element = product.find_element(*self.product_quantity)
        self.send_keys(quantity_element, str(quantity))
        self.click(self.update_cart_button)
        return self

    def click_update_cart(self):
        self.click(self.update_cart_button)
        return self
    
    def get_cart_total(self):
        total_text = self.total_amount_value
        return price_str_handle(total_text)
        
    def get_shipping_cost(self):
        shipping_text = self.flat_shipping_rate
        return price_str_handle(shipping_text)
    
    def get_products_count(self):
        products = self.get_all_products_in_cart()
        return len(products)
    
    def calculating_total_price(self):
        products = self.get_all_products_in_cart()
        total = 0.0
        for product in products:
            quantity = self.get_product_quantity(product)
            price = self.get_product_unit_price(product)
            try:
                total += quantity * price
            except ValueError:
                continue
        return total + self.get_shipping_cost()

    def get_product_by_position(self, position):
        products = self.get_all_products_in_cart()
        if 1 <= position < len(products):
            return products[position]
        else:
            raise IndexError("Неверная позиция продукта в корзине")
    
    def remove_product(self, product):
        remove_button = product.find_element(*self.remove_product_button)
        self.click(remove_button)

    def remove_even_products(self):
        i = 0

        while True:
            products = self.get_all_products_in_cart()
            if i + 1 >= len(products):
                break
            products[i + 1].find_element(*self.remove_product_button).click()
            i += 1                          
    
