from typing import Optional, List, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class BasePage:
    """Базовый класс для всех Page Object"""
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, timeout)
    
    @allure.step("Открыть URL: {url}")
    def open(self, url: str) -> 'BasePage':
        """Открыть указанный URL"""
        self.driver.get(url)
        return self
    
    @allure.step("Найти элемент по локатору: {by}={locator}")
    def find_element(self, by: str, locator: str, timeout: Optional[int] = None) -> WebElement:
        """Найти элемент с ожиданием"""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, locator)))
    
    @allure.step("Найти элементы по локатору: {by}={locator}")
    def find_elements(self, by: str, locator: str, timeout: Optional[int] = None) -> List[WebElement]:
        """Найти элементы с ожиданием"""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located((by, locator)))
    
    @allure.step("Кликнуть по элементу: {by}={locator}")
    def click_element(self, by: str, locator: str) -> 'BasePage':
        """Кликнуть по элементу"""
        element = self.find_element(by, locator)
        element.click()
        return self
    
    @allure.step("Ввести текст '{text}' в элемент: {by}={locator}")
    def type_text(self, by: str, locator: str, text: str) -> 'BasePage':
        """Ввести текст в поле"""
        element = self.find_element(by, locator)
        element.clear()
        element.send_keys(text)
        return self
    
    @allure.step("Сделать скриншот: {name}")
    def take_screenshot(self, name: str) -> str:
        """Сделать скриншот и прикрепить к Allure"""
        screenshot_path = f"screenshots/{name}.png"
        self.driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot_path