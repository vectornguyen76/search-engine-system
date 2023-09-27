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
            item_path=point["item_path"],
            item_image=point["item_image"],
            item_name=point["item_name"],
            fixed_item_price=point["fixed_item_price"],
            sale_item_price=point["sale_item_price"],
            sale_rate=point["sale_rate"],
            sales_number=point["sales_number"],
            shop_path=point["shop_path"],
            shop_name=point["shop_name"],
        )
