from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional

from constants import OutOfStock, SpecificPriceType


"""
The data classes can be changed and adapted to the needs of the developer and task
"""
class WeightUnit(Enum):
    KG = 1
    GR = 2


@dataclass
class Weight:
    value: Decimal
    weight_unit: WeightUnit = None


@dataclass
class Attribute:
    name: str
    position: Optional[str]
    lang_id: Optional[str] = None
    id: Optional[str] = None


@dataclass
class Stock:
    quantity: Optional[int]
    out_of_stock_action: Optional[OutOfStock]


@dataclass
class AttributeGroup:
    name: str
    attributes: Dict[str, Attribute]
    id: Optional[str] = None
    lang_id: Optional[str] = None

    def get_attribute_by(self, identifier: str) -> Attribute:
        return self.attributes[identifier]

    def get_identifier(self, identifier_name: str) -> str:
        return getattr(self, identifier_name)


@dataclass
class AttributePair:
    attribute: Attribute
    attribute_group: AttributeGroup


@dataclass
class Image:
    id: Optional[str]
    path: str
    name: Optional[str] = None
    position: Optional[str] = None
    base64_attachment: Optional[str] = None
    is_cover: bool = False


@dataclass
class Barcode:
    upc: Optional[str] = None
    ean_13: Optional[str] = None

    @property
    def value(self):
        return self.upc or self.ean_13


@dataclass
class SpecificPrice:
    amount_reduction: Optional[Decimal]
    reduction_type: SpecificPriceType
    id: Optional[str] = None
    country_id: Optional[str] = None
    customer_group_id: Optional[str] = None
    customer_id: Optional[str] = None
    from_quantity: Optional[int] = None
    percent_reduction: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class ManufacturerEntity:
    id: Optional[str]
    name: str
    lang_id: Optional[str]
    description: Optional[str]
    short_description: Optional[str]
    meta_title: Optional[str]
    meta_description: Optional[str]
    created_date: Optional[datetime]
    updated_date: Optional[datetime]
    is_active: Optional[bool]


@dataclass
class CategoryInfo:
    id: str
    name: Optional[str]
    lang_id: Optional[str]


@dataclass
class Variant:
    id: str
    price: Decimal
    stock: Stock
    sku: Optional[str]
    is_taxable: Optional[bool] = None
    specific_prices: List[SpecificPrice] = None
    images: List[Image] = None
    attribute_pairs: List[AttributePair] = None
    barcode: Barcode = Barcode(ean_13=None, upc=None)
    weight: Weight = Weight(value=None)


@dataclass
class Product:
    id: str
    name: str
    description: Optional[str]
    price: Decimal
    cost: Decimal
    images: List[Image]
    variants: List[Variant]
    tags: List[str]
    stock: Stock
    weight: Weight = Weight(value=None)
    barcode: Barcode = Barcode(ean_13=None, upc=None)
    manufacturers: List[ManufacturerEntity] = None
    specific_prices: List[SpecificPrice] = None
    is_active: bool = None
    is_virtual: bool = None
    categories: List[CategoryInfo] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    link_rewrite: Optional[str] = None
    sku: Optional[str] = None
    is_taxable: Optional[bool] = None
    link_rewrite: Optional[str] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    short_description: Optional[str] = None
    shop_id: Optional[str] = None
    lang_id: Optional[str] = None

