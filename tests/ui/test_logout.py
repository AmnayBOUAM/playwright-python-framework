import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = allure.feature("Connexion")


@pytest.mark.smoke
def test_deconnexion(inventory_page: InventoryPage):
    inventory_page.goto()
    inventory_page.logout()

    login_page = LoginPage(inventory_page.page)
    login_page.expect_displayed()


@pytest.mark.regression
def test_retour_arriere_apres_deconnexion(inventory_page: InventoryPage):
    inventory_page.goto()
    inventory_page.logout()
    inventory_page.page.go_back()

    expect(inventory_page.items).to_have_count(0)
