import random
import allure
from pages.cart_page import CartPage
from pages.header_page import HeaderPage
from pages.main_page import MainPage
from pages.product_page import ProductPage

from data.data import SORTING_OPTIONS


@allure.parent_suite("UI-тесты")
@allure.feature("Корзина")
@allure.story("Расчёт итоговой суммы корзины")
@allure.title("Должна корректно пересчитываться "
              "итоговая сумма после удаления товаров из корзины")
class TestCart:
    """Тесты для страницы корзины"""
    def test_cart_total_with_removals(self, driver):
        """Тест на расчёт суммы корзины после удаления товаров"""
        main_page = MainPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)

        for _ in range(5):

            main_page.open_main_page()

            products = main_page.get_product_names_in_home()

            random_product_position = random.randint(1, len(products) - 1)
            random_quantity = random.randint(1, 10)

            main_page.click_product_by_position_in_home(random_product_position)

            product_page.set_product_quantity_in_product_page(random_quantity)
            product_page.add_product_to_cart()

            cart_page.open_cart_page()

            assert cart_page.check_product_by_name(
                products[random_product_position].lower()
            ), (
                f"Продукт {products[random_product_position]} "
                f"не добавлен в корзину"
            )

        products_list_before_removal = cart_page.get_all_products_names_in_cart()

        cart_page.open_cart_page()
        cart_page.remove_even_products_from_cart()

        products_list_after_removal = cart_page.get_all_products_names_in_cart()

        assert products_list_before_removal[::2] == products_list_after_removal, (
            "Чётные продукты не удалены из корзины"
        )

        calculated_total, cart_total = cart_page.get_cart_totals()

        assert calculated_total == cart_total, (
            f"Расчитанная сумма корзины {calculated_total}"
            "не совпадает с фактической суммой {cart_total}"
        )

    @allure.story("Поиск товаров, добавление в корзину и проверка итоговой суммы")
    @allure.title("Должна корректно формироваться корзина и рассчитываться "
                "итоговая сумма после поиска и изменения количества товаров")
    def test_cart_total_with_search(self, driver):
        """Тест на добавление в корзину и проверку итоговой суммы"""
        main_page = MainPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        header_page = HeaderPage(driver)

        main_page.open_main_page()
        header_page.search_for_product("shirt")

        main_page.select_sorting_option(SORTING_OPTIONS[1])
        names_za = main_page.get_product_names_in_category()
        assert names_za == sorted(main_page.get_product_names_in_category(),
                                reverse=True), (
            "Товары не отсортированы по имени от Z до A"
        )

        main_page.click_product_by_position_in_category(2)

        product_page.set_product_quantity_in_product_page(22)

        product_page.add_product_to_cart()

        header_page.check_header_visible()
        header_page.search_for_product("shirt")

        main_page.select_sorting_option(SORTING_OPTIONS[1])

        assert names_za == sorted(main_page.get_product_names_in_category(),
                                reverse=True), (
            "Товары не отсортированы по имени от Z до A"
        )

        main_page.click_product_by_position_in_category(3)

        product_page.set_product_quantity_in_product_page(7)

        product_page.add_product_to_cart()

        cart_page.increase_cheapest_product_quantity()

        calculated_total, cart_total = cart_page.get_cart_totals()

        assert calculated_total == cart_total, (
            f"Расчитанная сумма корзины {calculated_total} "
            f"не совпадает с фактической суммой {cart_total}"
        )
