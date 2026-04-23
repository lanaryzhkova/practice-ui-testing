import allure

class Steps:
    @allure.step("Загрузка страницы корзины")
    def load_cart_page(self, cart_page):
        cart_page.load()

    @allure.step("Увеличение в 2 раза количества самого дешевого товара в корзине")
    def increase_cheapest_product_quantity(self, cart_page):
        cheapest_product = cart_page.cheapest_product()
        current_quantity = cart_page.get_product_quantity(cheapest_product)
        new_quantity = current_quantity * 2
        cart_page.change_product_quantity(new_quantity, cheapest_product)
        cart_page.click_update_cart()
        return self
    
    @allure.step("Получение рассчитанной и фактической суммы корзины")
    def get_cart_totals(self, cart_page):
        calculated_total = cart_page.calculating_total_price()
        cart_total = cart_page.get_cart_total()
        return calculated_total, cart_total
    
    @allure.step("Удаление продукта из корзины")
    def remove_product(self, cart_page):
        cart_page.remove_even_products()

    @allure.step("Получение списка всех продуктов в корзине")
    def get_all_products(self, cart_page):
        return cart_page.get_all_products_in_cart()
    
    @allure.step("Получение списка всех названий продуктов в корзине")
    def get_all_product_names(self, cart_page):
        products = cart_page.get_all_products_in_cart()
        product_names = []
        for product in products:
            product_name = cart_page.get_product_name(product)
            product_names.append(product_name)
        return product_names
    
    @allure.step("Проверка наличия продукта по имени в корзине")
    def check_product_by_name(self, cart_page, product_name):
        products = cart_page.get_all_products_in_cart()
        print(f"Проверяем наличие продукта '{product_name}' в корзине...")
        for product in products:
            name = cart_page.get_product_name(product).lower()
            if product_name in name:
                return True
        return False