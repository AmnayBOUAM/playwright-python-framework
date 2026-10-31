import allure
from playwright.sync_api import Page, expect

from data.users import User
from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def login(self, username: str, password: str) -> None:
        with allure.step(f"Se connecter avec '{username}'"):
            self.username_input.fill(username)
            self.password_input.fill(password)
            self.login_button.click()

    def login_as(self, user: User) -> None:
        self.login(user.username, user.password)

    def expect_error(self, text: str) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(text)

    def expect_displayed(self) -> None:
        expect(self.login_button).to_be_visible()
