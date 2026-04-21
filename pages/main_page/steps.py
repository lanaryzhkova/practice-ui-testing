import allure

class Steps:
    @allure.step("Загрузка главной страницы")
    def load_main_page(self, main_page):
        main_page.load()

    @allure.step("Выбор категории Fragrance")
    def select_category(self, main_page):
        main_page.click_category("FRAGRANCE")

    @allure.step("Сортировка по имени от A до Z")
    def sort_by_name_az(self, main_page):
        main_page.select_sorting_option("Name A - Z")
        return main_page.get_product_names_in_category()
        
    @allure.step("Сортировка по имени от Z до A")
    def sort_by_name_za(self, main_page):
        main_page.select_sorting_option("Name Z - A")
        return main_page.get_product_names_in_category()
        
    @allure.step("Сортировка по цене от низкой к высокой")
    def sort_by_price_low_high(self, main_page):
        main_page.select_sorting_option("Price Low > High")
        return main_page.get_product_prices()

    @allure.step("Сортировка по цене от высокой к низкой")
    def sort_by_price_high_low(self, main_page):
        main_page.select_sorting_option("Price High > Low")
        return main_page.get_product_prices()
        
    @allure.step("Выбор продукта по позиции {position} в категории")
    def select_product_by_position_in_category(self, main_page, position):
        main_page.click_product_by_position_in_category(position)

    @allure.step("Выбор продукта по позиции {position} на главной странице")
    def select_product_by_position_in_home(self, main_page, position):
        main_page.click_product_by_position_in_home(position)

    @allure.step("Поиск продукта {query}")
    def search_for_product(self, main_page, query):
        main_page.enter_search_query(query)
        main_page.submit_search()