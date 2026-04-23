from selenium.webdriver.remote.webelement import WebElement

def prices_array_handle(prices_text: list[str]) -> list[float]:
        return [float(price.replace("$", "")) for price in prices_text]

def price_str_handle(price_str: WebElement) -> float:
        return float(price_str.text.strip().replace("$", "").replace(",", ""))

