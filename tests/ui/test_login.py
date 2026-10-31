import allure
import pytest
from playwright.sync_api import expect

from data import users
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = allure.feature("Connexion")


@pytest.fixture(autouse=True)
def open_login(login_page: LoginPage) -> None:
    login_page.goto()


@pytest.mark.smoke
def test_connexion_reussie(login_page: LoginPage):
    login_page.login_as(users.STANDARD)

    inventory_page = InventoryPage(login_page.page)
    inventory_page.expect_loaded()
    expect(inventory_page.title).to_have_text("Products")


@pytest.mark.regression
@pytest.mark.parametrize(
    ("user", "error"),
    [
        (users.LOCKED_OUT, "Sorry, this user has been locked out."),
        (users.INVALID, "Username and password do not match"),
    ],
    ids=["utilisateur-bloque", "identifiants-invalides"],
)
def test_connexion_refusee(login_page: LoginPage, user, error: str):
    login_page.login_as(user)
    login_page.expect_error(error)
    expect(login_page.page).not_to_have_url("**/inventory.html")


@pytest.mark.regression
@pytest.mark.parametrize(
    ("username", "password", "error"),
    [
        ("", "x", "Username is required"),
        ("x", "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=["username-vide", "mot-de-passe-vide", "tout-vide"],
)
def test_champs_obligatoires(login_page: LoginPage, username: str, password: str, error: str):
    login_page.login(username, password)
    login_page.expect_error(error)


@pytest.mark.regression
def test_mot_de_passe_masque(login_page: LoginPage):
    expect(login_page.password_input).to_have_attribute("type", "password")


@pytest.mark.regression
def test_page_protegee_sans_session(login_page: LoginPage):
    login_page.page.goto("/inventory.html")
    login_page.expect_error("You can only access '/inventory.html' when you are logged in.")
