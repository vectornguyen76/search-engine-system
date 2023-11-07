from src.models import CustomModel


class SearchData(CustomModel):
    user_id: int
    search_query: str
    size: int = 20


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
