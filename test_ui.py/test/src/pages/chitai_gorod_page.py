from typing import List, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import allure
from src.pages.base_page import BasePage


class ChitaiGorodPage(BasePage):
    """Page Object для сайта Читай-город"""
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.base_url: str = "https://www.chitai-gorod.ru/"
    
    # Локаторы
    COOKIE_ACCEPT_BUTTON: str = "//button[contains(text(), 'Принять') or contains(text(), 'Согласен')]"
    SEARCH_INPUT: str = "input[type='search'], input[placeholder*='поиск']"
    SEARCH_BUTTON: str = "button[type='submit'], .search-btn"
    PRODUCT_CARDS: str = ".product-card, .book-item, .item-card"
    NAVIGATION_LINKS: str = "nav a, .menu-item, .header__menu-item"
    
    @allure.step("Открыть главную страницу Читай-город")
    def open_main_page(self) -> 'ChitaiGorodPage':
        """Открыть главную страницу"""
        self.open(self.base_url)
        return self
    
    @allure.step("Принять cookies")
    def accept_cookies(self) -> 'ChitaiGorodPage':
        """Принять cookies если появилось окно"""
        try:
            self.click_element(By.XPATH, self.COOKIE_ACCEPT_BUTTON)
            allure.attach("Cookies accepted", "Уведомление о cookies принято", allure.attachment_type.TEXT)
        except:
            allure.attach("No cookies popup", "Окно cookies не появилось", allure.attachment_type.TEXT)
        return self
    
    @allure.step("Выполнить поиск: '{query}'")
    def search_products(self, query: str) -> 'ChitaiGorodPage':
        """Выполнить поиск товаров"""
        try:
            self.type_text(By.CSS_SELECTOR, self.SEARCH_INPUT, query)
            self.find_element(By.CSS_SELECTOR, self.SEARCH_INPUT).send_keys(Keys.ENTER)
        except:
            # Альтернативный способ поиска
            search_btn = self.find_element(By.CSS_SELECTOR, self.SEARCH_BUTTON)
            search_btn.click()
        return self
    
    @allure.step("Получить результаты поиска")
    def get_search_results(self) -> List[str]:
        """Получить список найденных товаров"""
        try:
            products = self.find_elements(By.CSS_SELECTOR, self.PRODUCT_CARDS)
            return [product.text for product in products if product.text.strip()]
        except:
            return []
    
    @allure.step("Получить элементы навигации")
    def get_navigation_items(self) -> List[str]:
        """Получить элементы навигации"""
        try:
            nav_items = self.find_elements(By.CSS_SELECTOR, self.NAVIGATION_LINKS)
            return [item.text for item in nav_items if item.text.strip()]
        except:
            return []
    
    @allure.step("Проверить заголовок страницы")
    def get_page_title(self) -> str:
        """Получить заголовок страницы"""
        return self.driver.title
    
    @allure.step("Проверить текущий URL")
    def get_current_url(self) -> str:
        """Получить текущий URL"""
        return self.driver.current_url