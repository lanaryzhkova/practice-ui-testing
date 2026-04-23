from selenium.webdriver.remote.webelement import WebElement


def prices_array_handle(prices_text: list[str]) -> list[float]:
    """Преобразование массива строковых цен в массив чисел"""
    return [float(price.replace("$", "")) for price in prices_text]


def price_str_handle(price_str: WebElement) -> float:
    """Преобразование строки цены в число"""
    return float(price_str.text.strip().replace("$", "").replace(",", ""))
