from pydantic import BaseModel, Field

class Product(BaseModel):
    item_url: str
    item_image: str
    item_name: str
    item_price: str

    @classmethod
    def from_point(cls, point) -> "Product":
        return Product(
            item_url=point.payload["item_url"].string_value,
            item_image=point.payload["item_image"].string_value,
            item_name=point.payload["item_name"].string_value,
            item_price=point.payload["item_price"].string_value,
        )
        
    @classmethod
    def from_point(cls, point) -> "Product":
        return Product(
            item_url=point.payload["item_url"].string_value,
            item_image=point.payload["item_image"].string_value,
            item_name=point.payload["item_name"].string_value,
            item_price=point.payload["item_price"].string_value,
        )