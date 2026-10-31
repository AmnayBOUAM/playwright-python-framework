from typing import Literal

import allure
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from utils.helpers import parse_price

SortOption = Literal["az", "za", "lohi", "hilo"]


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.item_images = self.items.locator("img")
        self.sort_select = page.get_by_test_id("product-sort-container")

    def item(self, name: str) -> Locator:
        return self.items.filter(has=self.page.get_by_text(name, exact=True))

    def add_to_cart(self, name: str) -> None:
        with allure.step(f"Ajouter '{name}' au panier"):
            self.item(name).get_by_role("button", name="Add to cart").click()

    def add_all_to_cart(self, names: list[str]) -> None:
        for name in names:
            self.add_to_cart(name)

    def remove_from_cart(self, name: str) -> None:
        with allure.step(f"Retirer '{name}' du panier"):
            self.item(name).get_by_role("button", name="Remove").click()

    def open_product(self, name: str) -> None:
        with allure.step(f"Ouvrir la fiche de '{name}'"):
            self.item(name).get_by_test_id("inventory-item-name").click()

    def sort_by(self, option: SortOption) -> None:
        with allure.step(f"Trier par '{option}'"):
            self.sort_select.select_option(option)

    def get_names(self) -> list[str]:
        return self.item_names.all_text_contents()

    def get_prices(self) -> list[float]:
        return [parse_price(t) for t in self.item_prices.all_text_contents()]

    def get_price(self, name: str) -> float:
        return parse_price(self.item(name).get_by_test_id("inventory-item-price").text_content())

    def get_image_sources(self) -> list[str]:
        return [img.get_attribute("src") or "" for img in self.item_images.all()]
