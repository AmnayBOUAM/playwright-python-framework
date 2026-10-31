from collections.abc import Iterator

import allure
import pytest
from playwright.sync_api import Browser, Page

from config import settings
from data import users
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


# login une seule fois pour toute la session, les tests réutilisent le storage_state
@pytest.fixture(scope="session")
def auth_state(browser: Browser) -> str:
    context = browser.new_context(base_url=settings.SAUCEDEMO_URL)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login_as(users.STANDARD)
    InventoryPage(page).expect_loaded()

    settings.STORAGE_STATE.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=settings.STORAGE_STATE)
    context.close()
    return str(settings.STORAGE_STATE)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, auth_state: str) -> dict:
    return {**browser_context_args, "base_url": settings.SAUCEDEMO_URL, "storage_state": auth_state}


@pytest.fixture(autouse=True)
def default_timeout(page: Page) -> None:
    page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)


# pour les tests de login : contexte sans session
@pytest.fixture
def guest_page(browser: Browser, browser_context_args: dict) -> Iterator[Page]:
    context = browser.new_context(**{**browser_context_args, "storage_state": None})
    page = context.new_page()
    page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    yield page
    context.close()


@pytest.fixture
def login_page(guest_page: Page) -> LoginPage:
    return LoginPage(guest_page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


# capture d'écran dans Allure quand un test échoue
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    seen: set[int] = set()
    for value in getattr(item, "funcargs", {}).values():
        page = value if isinstance(value, Page) else getattr(value, "page", None)
        if isinstance(page, Page) and id(page) not in seen and not page.is_closed():
            seen.add(id(page))
            allure.attach(
                page.screenshot(full_page=True),
                name=f"Capture - {page.url}",
                attachment_type=allure.attachment_type.PNG,
            )
