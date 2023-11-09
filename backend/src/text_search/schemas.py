from src.models import CustomModel


class SearchResponse(CustomModel):
    item_path: str
    item_image: str
    item_name: str
    fixed_item_price: int
    sale_item_price: int
    sale_rate: float
    sales_number: int
    shop_path: str
    shop_name: str
