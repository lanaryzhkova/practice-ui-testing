from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # без UI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()