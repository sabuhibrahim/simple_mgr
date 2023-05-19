import requests
from datetime import datetime
from typing import List
from cart import Cart
from product import (
    Product, 
    CategoryInfo, 
    Variant, 
    Image, 
    SpecificPrice,
    Barcode,
    Stock,
    Weight,
    WeightUnit,
    AttributePair,
    Attribute,
    AttributeGroup,
    ManufacturerEntity,
)

from constants import OutOfStock

import json

class ShopifyImporter:
    
    PRODUCT_LIST_API = "/admin/api/2023-04/products.json"

    def __init__(self, cart: Cart) -> None:
        self.cart = cart

    def start(self) -> List[Product]:
        products: List[Product] = []
        
        # implement the importer logic here

        data = self.get_product_data()
        for item in data:
            first_variant = item["variants"][0] if item["variants"] else None

            price = None
            cost = None
            is_virtual = False
            sku = None
            stock = None

            if first_variant:
                price = first_variant["compare_at_price"] or first_variant["price"]
                is_virtual = first_variant.get("requires_shipping", False)
                sku = first_variant["sku"]
                stock = Stock(
                    quantity=first_variant["inventory_quantity"],
                    out_of_stock_action=OutOfStock[first_variant["inventory_policy"].upper()]
                )
            
            product_attribute_groups: List[AttributeGroup] = self.set_product_attribute_groups(item["options"])

            product_images: List[Image] = self.get_images_obj_list(item["images"])
            
            products.append(
                Product(
                    id=item["id"],
                    name=item["title"],
                    description=item["body_html"],
                    short_description=item["body_html"], # couldn't find short description info
                    shop_id=item["vendor"],
                    lang_id=item["vendor"], # couldn't find lang info
                    meta_title=item["title"], # couldn't find meta title info
                    meta_description=item["body_html"], # couldn't find meta description info
                    link_rewrite=item["handle"],
                    price=price,
                    cost=cost,
                    is_active=item["status"] == "active",
                    is_virtual=is_virtual,
                    images=product_images,
                    sku=sku,
                    variants=[
                        Variant(
                            id=variant["id"],
                            price=variant["compare_at_price"] or variant["price"],
                            stock=Stock(
                                quantity=variant["inventory_quantity"],
                                out_of_stock_action=OutOfStock[variant["inventory_policy"].upper()]
                            ),
                            sku=variant["sku"],
                            specific_prices=variant["price"] if variant["compare_at_price"] else None,
                            images=[product_images],
                            attribute_pairs=self.get_variant_atribute_pairs_list(product_attribute_groups, variant),
                            barcode=variant["barcode"],
                            weight=Weight(value=variant["weight"], weight_unit=WeightUnit[variant["weight_unit"].upper()]),
                        ) for variant in item["variants"]
                    ],
                    manufacturers=[ManufacturerEntity(
                        id=None,
                        name=item["vendor"],
                        lang_id=None,
                        description=None,
                        short_description=None,
                        meta_title=None,
                        meta_description=None,
                        created_date=None,
                        updated_date=None,
                        is_active=None,
                    )],
                    categories=[], # CategoryInfo
                    specific_prices=[],
                    tags=[],
                    is_taxable=None,
                    stock=stock,
                    created_date=datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%S%z"),
                    updated_date=datetime.strptime(item["updated_at"], "%Y-%m-%dT%H:%M:%S%z"),
                    weight=Weight(value=first_variant["weight"], weight_unit=WeightUnit[first_variant["weight_unit"].upper()]),
                    barcode=Barcode(upc=first_variant["barcode"], ean_13=None),
                )
            )
        
        print(products)

        return products
    

    def get_product_data(self) -> list:
        url = self.cart.url + self.PRODUCT_LIST_API
        
        response = requests.get(
            url=url, 
            headers={
                "X-Shopify-Access-Token": self.cart.token,
                "Content-type": "application/json",
            }
        )

        if response.status_code not in [200, 201]:
            raise Exception(
                "An error occured when getting product data. "
                f"url = {url}, "
                f"response status code = {response.status_code}"
            )
        
        return response.json()["products"]
    

    def get_images_obj_list(self, images: List[dict]) -> List[Image]:
        return [
            Image(
                id=image["id"],
                name=image.get("name", None),
                position=image["position"],
                path=image["src"],
                base64_attachment=image.get("base64_attachment", None),
                is_cover=image.get("is_cover", False),
            ) for image in images
        ]
    

    def set_product_attribute_groups(self, options: List[dict]) -> List[AttributeGroup]:
        
        attribute_group_list: List[AttributeGroup] = []
        
        for option in options:
            atribute_dict: dict[str, Attribute] = (
                { attr: Attribute(name=attr, id=None, position=None, lang_id=None) for attr in option["values"] }
            )
            attribute_group_list.append(
                AttributeGroup(
                    id=option["id"],
                    name=option["name"],
                    lang_id=None,
                    attributes=atribute_dict  
                )
            )
        
        return attribute_group_list

    

    def get_variant_atribute_pairs_list(
        self, product_attribute_groups: List[AttributeGroup], variant_data: dict
    ) -> List[AttributePair]:
        atribute_pair_list: List[AttributePair] = []
        
        for attr_group in product_attribute_groups:
            values = attr_group.attributes.keys()
            if variant_data["option1"] and variant_data["option1"] in values:
                atribute_pair_list.append(
                    AttributePair(
                        attribute=Attribute(name=variant_data["option1"], id=None, position=None, lang_id=None),
                        attribute_group=attr_group,
                    )
                )
            
            if variant_data["option2"] and variant_data["option2"] in values:
                atribute_pair_list.append(
                    AttributePair(
                        attribute=Attribute(name=variant_data["option2"], id=None, position=None, lang_id=None),
                        attribute_group=attr_group,
                    )
                )
            
            if variant_data["option3"] and variant_data["option3"] in values:
                atribute_pair_list.append(
                    AttributePair(
                        attribute=Attribute(name=variant_data["option3"], id=None, position=None, lang_id=None),
                        attribute_group=attr_group,
                    )
                )
        
        return atribute_pair_list

def get_importer(cart):
    return ShopifyImporter(cart)