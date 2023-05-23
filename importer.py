from typing import List
import requests

from cart import Cart
from product import *


class ShopifyImporter:
    def __init__(self, cart: Cart) -> None:
        self.cart = cart

    def start(self) -> List[Product]:
        products: List[Product] = []

        # implement the importer logic here
        shopify_response = requests.get(self.cart.url + "/admin/api/2023-04/products.json", headers={"X-Shopify-Access-Token":self.cart.token})
        for item in shopify_response.json()["products"]:
            # add images
            images: List[Image] = []
            for image in item["images"]:
                images.append(Image(id=image["id"], position=image["position"], path=image["src"]))

            # add variants
            specific_prices = []
            variants: List[Variant] = []
            for variant in item["variants"]:
                weight = Weight(value=variant["weight"])
                barcode = Barcode(upc=variant["barcode"])
                stock = Stock(quantity=variant["inventory_quantity"], out_of_stock_action=variant["old_inventory_quantity"])

                attribute_pairs = []
                specific_prices = []

                # create attribute_pairs
                for option in item["options"]:
                    position_key = "option"+str(option["position"])
                    value = variant[position_key]
                    attribute = Attribute(name=value, position=option["position"])
                    attributes = []

                    for attrib in option["values"]:
                        attributes.append({option["position"]: Attribute(name=attrib, position=option["position"])})

                    attribute_group = AttributeGroup(id=option["id"], name=option["name"], attributes=attributes)
                    attribute_pairs.append(AttributePair(attribute=attribute, attribute_group=attribute_group))
                
                specific_price = SpecificPrice(amount_reduction=Decimal(variant["compare_at_price"])-Decimal(variant["price"]), reduction_type=SpecificPriceType.AMOUNT)
                specific_prices.append(specific_price)

                # create variant model
                variant_obj = Variant(id=variant["id"],
                                price=variant["price"],
                                sku=variant["sku"],
                                is_taxable=variant["taxable"],
                                barcode=barcode,
                                weight=weight, stock=stock,
                                attribute_pairs=attribute_pairs,
                                specific_prices=specific_prices)

                variants.append(variant_obj)
                
            # add total product
            products.append(Product(id=item["id"], name=item["title"],
                                    description=item["body_html"], created_date=item["created_at"],
                                    updated_date=item["updated_at"],
                                    meta_title=item["title"], meta_description=item["body_html"], images=images, 
                                    price=variants[0].price, cost=item["variants"][0]["compare_at_price"],
                                    sku=variants[0].sku, is_taxable=variants[0].is_taxable, variants=variants,
                                    weight=variants[0].weight, barcode=variants[0].barcode, stock=variants[0].stock,
                                    tags=item["tags"], specific_prices=specific_prices))
            
        print(products[1])
        return products


def get_importer(cart):
    return ShopifyImporter(cart)