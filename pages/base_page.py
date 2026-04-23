from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from utils.wait_helper import WaitHelper
from data.data import BASE_URL


class BasePage:
    """Базовый класс"""
    def __init__(self, driver):
        """Инициализация базового класса"""
        self.driver = driver
        self.base_url = BASE_URL
        self.wait = WaitHelper(driver, 10)

    def open(self, url: str) -> 'BasePage':
        """Открывает страницу по ссылке"""
        self.driver.get(url or self.base_url)
        return self

    def find_element(self, locator: tuple) -> WebElement:
        """Поиск элемента по локатору"""
        return self.wait.wait_for_element_visible(locator)

    def find_elements(self, locator: tuple) -> list[WebElement]:
        """Поиск элементов по локатору"""
        return self.wait.wait_for_all_elements_visible(locator)

    def scroll_to(self, elem) -> 'BasePage':
        """Прокрутка до элемента"""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'start'});",
            elem
        )
        return self

    def click(self, element: WebElement) -> 'BasePage':
        """Метод нажатия на элемент"""
        elem = element
        self.scroll_to(elem)
        elem.click()
        return self

    def send_keys_to_input(self, locator: tuple, text: str):
        """Метод для ввода текста"""
        elem = self.wait.wait_for_element_clickable(locator)
        elem.clear()
        elem.send_keys(text)
        return self

    def text_of(self, element: WebElement) -> str:
        """Метод получения текста элемента"""
        return element.text.strip()

    def is_visible(self, locator: tuple) -> bool:
        """Метод проверки видимости элемента"""
        try:
            self.wait.wait_for_element_visible(locator)
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False

    def get_attribute_of_element(self,
                                 element: WebElement,
                                 attribute: str) -> str | int | float | None:
        """Метод получения атрибута элемента"""
        return element.get_attribute(attribute)

    def get_current_url(self) -> str:
        """Метод получения текущего URL"""
        return self.driver.current_url
