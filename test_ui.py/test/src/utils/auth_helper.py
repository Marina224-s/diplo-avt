from typing import Dict, Any
from selenium.webdriver.remote.webdriver import WebDriver
import allure


class AuthHelper:
    """Вспомогательный класс для работы с авторизацией"""
    
    @staticmethod
    @allure.step("Установить auth cookie для пользователя")
    def set_auth_cookie(driver: WebDriver, auth_token: str, domain: str = "chitai-gorod.ru") -> None:
        """
        Установить cookie авторизации для избежания UI-авторизации
        
        Args:
            driver: WebDriver instance
            auth_token: Токен авторизации
            domain: Домен для cookie
        """
        cookie = {
            'name': 'auth_token',
            'value': auth_token,
            'domain': domain,
            'path': '/',
            'secure': True
        }
        
        driver.add_cookie(cookie)
        allure.attach(f"Auth cookie set: {auth_token}", "Cookie установлен", allure.attachment_type.TEXT)