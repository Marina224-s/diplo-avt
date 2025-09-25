import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def page(driver):
    from tests.test_ui import ChitaiGorodPage
    return ChitaiGorodPage(driver)