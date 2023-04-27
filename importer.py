from typing import List

from cart import Cart
from product import Product


class ShopifyImporter:
    def __init__(self, cart: Cart) -> None:
        self.cart = cart

    def start(self) -> List[Product]:
        products: List[Product] = []

        # implement the importer logic here

        return products


def get_importer(cart):
    return ShopifyImporter(cart)