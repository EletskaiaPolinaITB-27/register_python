from datetime import datetime
from pydantic import BaseModel

class ProductCreateUpdateSchema(BaseModel):
    name: str
    price: float

class ProductSchema(ProductCreateUpdateSchema):
    id: int
    created_at: datetime | None = None
