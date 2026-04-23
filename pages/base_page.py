from selenium.common import NoSuchElementException, TimeoutException

from utils.wait_helper import WaitHelper
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from data.data import BASE_URL

class BasePage:
    def __init__(self, driver):
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

    def click(self, element_or_locator) -> 'BasePage':
        if isinstance(element_or_locator, tuple):
            elem = self.wait.wait_for_element_clickable(element_or_locator)
        else:
            elem = element_or_locator
        self.scroll_to(elem)
        elem.click()
        return self

    def send_keys_to_input(self, locator: tuple, text: str):
        elem = self.wait.wait_for_element_clickable(locator)
        elem.clear()
        elem.send_keys(text)
        return self

    def text_of(self, element_or_locator) -> str:
        if isinstance(element_or_locator, tuple):
            elem = self.find_element(element_or_locator)
            return elem.text.strip()   
        else:
            return element_or_locator.text.strip()

    def is_visible(self, locator: tuple) -> bool:
        try:
            self.wait.wait_for_element_visible(locator)
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False

    def get_attribute_of_element(self, element_or_locator, attribute_name: str) -> str|int|float|None:
        if isinstance(element_or_locator, tuple):
            elem = self.find_element(element_or_locator)
            return elem.get_attribute(attribute_name)
        else:
            return element_or_locator.get_attribute(attribute_name)
        
    def get_text(self, element_or_locator: tuple | WebElement) -> str:
        if isinstance(element_or_locator, tuple):
            elem = self.find_element(element_or_locator)
            return elem.text.strip()
        else:
            return element_or_locator.text.strip()
        
    def get_current_url(self) -> str:
        return self.driver.current_url