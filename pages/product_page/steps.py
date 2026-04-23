import allure

class Steps:
    @allure.step("Ввод количества товара {quantity} в поле количества")
    def set_product_quantity(self, product_page, quantity):
        product_page.set_product_quantity(quantity)
        return self
    
    @allure.step("Добавление товара в корзину")
    def add_product_to_cart(self, product_page):
        product_page.add_product_to_cart()
        return self