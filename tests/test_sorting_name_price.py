from pages.main_page import MainPage
import allure
from data.data import SORTING_OPTIONS

@allure.parent_suite("UI-тесты")
@allure.feature("Сортировка товаров")
@allure.story("Сортировка товаров по имени и цене")
@allure.title("Должна корректно работать сортировка товаров по имени и цене в обоих направлениях")

def test_sorting_by_name(driver):
    main_page = MainPage(driver)

    main_page.open_main_page()
    main_page.click_category("FRAGRANCE")

    main_page.select_sorting_option(SORTING_OPTIONS[0])
    namesAZ = main_page.get_product_names_in_category()
    assert namesAZ == sorted(namesAZ), "Товары не отсортированы по имени от A до Z"

    namesZA = main_page.select_sorting_option(SORTING_OPTIONS[1])
    namesZA = main_page.get_product_names_in_category()
    assert namesZA == sorted(namesZA, reverse=True), "Товары не отсортированы по имени от Z до A"

    main_page.select_sorting_option(SORTING_OPTIONS[2])
    pricesLH = main_page.get_product_prices_in_category()
    assert pricesLH == sorted(pricesLH), "Товары не отсортированы по цене от низкой к высокой"

    main_page.select_sorting_option(SORTING_OPTIONS[3])
    pricesHL = main_page.get_product_prices_in_category()
    assert pricesHL == sorted(pricesHL, reverse=True), "Товары не отсортированы по цене от высокой к низкой"
