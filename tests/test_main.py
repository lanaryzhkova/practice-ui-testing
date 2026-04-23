import allure

from pages.main_page import MainPage

from data.data import SORTING_OPTIONS


@allure.parent_suite("UI-тесты")
@allure.feature("Сортировка товаров")
@allure.story("Сортировка товаров по имени и цене")
@allure.title("Должна корректно работать сортировка товаров "
              "по имени и цене в обоих направлениях")
class TestMain:
    """Тесты для главной страницы"""
    def test_sorting_by_name(self, driver):
        """Тест на сортировку товаров по цене и стоимости"""
        main_page = MainPage(driver)

        main_page.open_main_page()
        main_page.click_category("FRAGRANCE")

        main_page.select_sorting_option(SORTING_OPTIONS[0])
        names_az = main_page.get_product_names_in_category()
        assert names_az == sorted(names_az), (
            "Товары не отсортированы по имени от A до Z"
            )

        names_za = main_page.select_sorting_option(SORTING_OPTIONS[1])
        names_za = main_page.get_product_names_in_category()
        assert names_za == sorted(names_za, reverse=True), (
            "Товары не отсортированы по имени от Z до A"
            )

        main_page.select_sorting_option(SORTING_OPTIONS[2])
        prices_lh = main_page.get_product_prices_in_category()
        assert prices_lh == sorted(prices_lh), (
            "Товары не отсортированы по цене от низкой к высокой"
            )

        main_page.select_sorting_option(SORTING_OPTIONS[3])
        prices_hl = main_page.get_product_prices_in_category()
        assert prices_hl == sorted(prices_hl, reverse=True), (
            "Товары не отсортированы по цене от высокой к низкой"
        )
