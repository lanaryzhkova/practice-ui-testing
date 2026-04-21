from pages.cart_page.cart_page import CartPage
from pages.components.header.header_page import HeaderPage
from pages.main_page.main_page import MainPage
from pages.main_page.steps import Steps as MainSteps
from pages.product_page.steps import Steps as ProductSteps
from pages.cart_page.steps import Steps as CartSteps
from pages.components.header.steps import Steps as HeaderSteps
import allure

from pages.product_page.product_page import ProductPage

@allure.parent_suite("UI-тесты")
@allure.feature("Поиск товаров и работа с корзиной")
@allure.story("Поиск товаров, добавление в корзину и проверка итоговой суммы")
@allure.title("Должна корректно формироваться корзина и рассчитываться итоговая сумма после поиска и изменения количества товаров")

def test_cart_total_with_search(driver):
    main_page = MainPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    header_page = HeaderPage(driver)
    main_steps = MainSteps()
    header_steps = HeaderSteps()
    product_steps = ProductSteps()
    cart_steps = CartSteps()

    main_steps.load_main_page(main_page)
    header_steps.search_for_product(header_page, "shirt")

    namesZA = main_steps.sort_by_name_za(main_page)
    assert namesZA == sorted(namesZA, reverse=True), "Товары не отсортированы по имени от Z до A"

    main_steps.select_product_by_position_in_category(main_page, 2)

    product_steps.set_product_quantity(product_page, 22)

    product_steps.add_product_to_cart(product_page)

    main_steps.load_main_page(main_page)
    header_steps.search_for_product(header_page, "shirt")

    namesZA = main_steps.sort_by_name_za(main_page)
    assert namesZA == sorted(namesZA, reverse=True), "Товары не отсортированы по имени от Z до A"

    main_steps.select_product_by_position_in_category(main_page, 3)

    product_steps.set_product_quantity(product_page, 7)

    product_steps.add_product_to_cart(product_page)

    cart_steps.increase_cheapest_product_quantity(cart_page)

    calculated_total, cart_total = cart_steps.get_cart_totals(cart_page)

    assert calculated_total == cart_total, f"Расчитанная сумма корзины {calculated_total} не совпадает с фактической суммой {cart_total}"