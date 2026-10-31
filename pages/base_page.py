import re

import allure
from playwright.sync_api import Page, expect


class BasePage:

    path = "/"

    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")
        self.reset_link = page.get_by_test_id("reset-sidebar-link")

    def goto(self) -> None:
        with allure.step(f"Ouvrir {self.path}"):
            self.page.goto(self.path)

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(self.path)))

    def open_cart(self) -> None:
        self.cart_link.click()

    def cart_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.text_content() or 0)

    def logout(self) -> None:
        with allure.step("Se déconnecter"):
            self.menu_button.click()
            self.logout_link.click()
