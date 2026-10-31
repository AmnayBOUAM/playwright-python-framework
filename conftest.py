import pytest
from playwright.sync_api import Playwright

from config import settings


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright: Playwright) -> None:
    playwright.selectors.set_test_id_attribute(settings.TEST_ID_ATTRIBUTE)

