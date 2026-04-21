from pages.main_page.main_page import MainPage
from pages.main_page.steps import Steps
import allure


@allure.feature("Сортировка товаров")
@allure.story("Сортировка товаров по имени и цене")

def test_sorting_by_name(driver):
    main_page = MainPage(driver)
    steps = Steps()
    steps.load_main_page(main_page)
    steps.select_category(main_page)

    namesAZ = steps.sort_by_name_az(main_page)
    print("Полученные имена продуктов после сортировки A-Z:", namesAZ)  # Debug print
    print("Ожидаемые имена продуктов после сортировки A-Z:", sorted(namesAZ))  # Debug print
    assert namesAZ == sorted(namesAZ), "Товары не отсортированы по имени от A до Z"

    namesZA = steps.sort_by_name_za(main_page)
    print("Полученные имена продуктов после сортировки Z-A:", namesZA)  # Debug print
    print("Ожидаемые имена продуктов после сортировки Z-A:", sorted(namesZA, reverse=True))  # Debug print
    assert namesZA == sorted(namesZA, reverse=True), "Товары не отсортированы по имени от Z до A"

    pricesLH = steps.sort_by_price_low_high(main_page)
    assert pricesLH == sorted(pricesLH), "Товары не отсортированы по цене от низкой к высокой"

    pricesHL = steps.sort_by_price_high_low(main_page)
    assert pricesHL == sorted(pricesHL, reverse=True), "Товары не отсортированы по цене от высокой к низкой"
