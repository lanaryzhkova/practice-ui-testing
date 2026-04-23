import allure

class Steps:
    @allure.step("Поиск товара '{search_query}'")
    def search_for_product(self, header_page, search_query):
        header_page.search_for_product(search_query)