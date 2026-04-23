import random

from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.product_page import ProductPage

import allure

@allure.parent_suite("UI-тесты")
@allure.feature("Расчёт итоговой суммы корзины")
@allure.story("Расчёт итоговой суммы корзины")
@allure.title("Должна корректно пересчитываться итоговая сумма после удаления товаров из корзины")

def test_cart_total_with_removals(driver):
    main_page = MainPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    for i in range(5):

        main_page.open_main_page()

        products = main_page.get_product_names_in_home()

        random_product_position = random.randint(1, len(products) - 1)
        random_quantity = random.randint(1, 10)

        main_page.click_product_by_position_in_home(random_product_position)

        product_page.set_product_quantity_in_product_page(random_quantity)
        product_page.add_product_to_cart()

        cart_page.open_cart_page()
        
        assert cart_page.check_product_by_name(products[random_product_position].lower()), f"Продукт {products[random_product_position]} не добавлен в корзину"

    products_list_before_removal = cart_page.get_all_products_names_in_cart()

    cart_page.open_cart_page()
    cart_page.remove_even_products_from_cart()

    products_list_after_removal = cart_page.get_all_products_names_in_cart()

    assert products_list_before_removal[::2] == products_list_after_removal, "Чётные продукты не удалены из корзины"

    calculated_total, cart_total = cart_page.get_cart_totals()
    
    assert calculated_total == cart_total, f"Расчитанная сумма корзины {calculated_total} не совпадает с фактической суммой {cart_total}"