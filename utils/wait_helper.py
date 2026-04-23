from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WaitHelper:
    """Хелперы для ожидания элементов"""
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element_visible(self, locator):
        """Ожидает, пока элемент станет видимым на странице"""
        return self.wait.until(EC.visibility_of_element_located(locator),
                               message=f"Элемент с локатором {locator} не виден")

    def wait_for_all_elements_visible(self, locator):
        """Ожидает, пока все элементы по локатору станут видимыми"""
        return self.wait.until(EC.visibility_of_all_elements_located(locator),
                               message=f"Элементы с локатором {locator} не видны")

    def wait_for_element_clickable(self, locator):
        """Ожидает, пока элемент станет кликабельным"""
        return self.wait.until(EC.element_to_be_clickable(locator),
                               message=f"Элемент с локатором {locator} не кликабелен")

    def wait_for_element_present(self, locator):
        """Ожидает, пока элемент появится в DOM"""
        return self.wait.until(EC.presence_of_element_located(locator),
                               message=f"Элемент с локатором {locator} не найден")

    def wait_for_url(self, url: str):
        """Ожидает, пока текущий URL страницы станет равен указанному"""
        return self.wait.until(
            EC.url_to_be(url),
            message=f"Ожидался URL {url}, но получен {self.driver.current_url}"
        )
