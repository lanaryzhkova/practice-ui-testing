import random

from data.data import BASE_URL
from pages.cart_page.cart_page import CartPage
from pages.main_page.main_page import MainPage
from pages.product_page.product_page import ProductPage
from pages.main_page.steps import Steps as MainSteps
from pages.product_page.steps import Steps as ProductSteps
from pages.cart_page.steps import Steps as CartSteps

import allure

@allure.feature("Проверка поисковой выдачи и корзины")
@allure.story("")

def test_cart_total_with_removals(driver):
    main_page = MainPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    main_steps = MainSteps()
    product_steps = ProductSteps()
    cart_steps = CartSteps()

    for i in range(5):

        main_page.load()

        products = main_page.get_product_names_in_home()

        random_product_position = random.randint(1, len(products) - 1)
        random_quantity = random.randint(1, 10)

        main_steps.select_product_by_position_in_home(main_page, random_product_position)

        product_steps.set_product_quantity(product_page, random_quantity)
        product_steps.add_product_to_cart(product_page)

    cart_page.load()
    cart_steps.remove_product(cart_page)

    calculated_total, cart_total = cart_steps.get_cart_totals(cart_page)
    
    assert calculated_total == cart_total, f"Расчитанная сумма корзины {calculated_total} не совпадает с фактической суммой {cart_total}"