from pydantic import BaseModel


class Product(BaseModel):
    item_path: str
    item_image: str
    item_name: str
    fixed_item_price: int
    sale_item_price: int
    sale_rate: float
    sales_number: int
    shop_path: str
    shop_name: str

    @classmethod
    def from_point(cls, point) -> "Product":
        return Product(
            item_path=point.payload["item_path"].string_value,
            item_image=point.payload["item_image"].string_value,
            item_name=point.payload["item_name"].string_value,
            fixed_item_price=point.payload["fixed_item_price"].integer_value,
            sale_item_price=point.payload["sale_item_price"].integer_value,
            sale_rate=point.payload["sale_rate"].double_value,
            sales_number=point.payload["sales_number"].integer_value,
            shop_path=point.payload["shop_path"].string_value,
            shop_name=point.payload["shop_name"].string_value,
        )
