from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.products.models import Product
from src.products.schemas import ProductSchema, ProductCreateUpdateSchema


product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
)



@product_router.get("/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)) ->List[ProductSchema]:
    return db.query(Product).filter_by(is_available=True)




@product_router.get("/{id}", response_model=ProductSchema)
def get_product(id: int, db: Session = Depends(get_db)) -> ProductSchema:
    product = db.query(Product).filter_by(id=id, is_available=True).first()
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")




@product_router.post("/")
def create_product(
    product: ProductCreateUpdateSchema,
    db: Session = Depends(get_db)
) -> ProductSchema:
    new_product = Product(**product.model_dump(exclude_unset=True))
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product




@product_router.put("/{id}", response_model=ProductSchema)
def update_product(
    id: int,
    product: ProductCreateUpdateSchema,
    db: Session = Depends(get_db)
) -> ProductSchema:
    new_product = db.query(Product).get(id)
    if new_product:
        new_product.update(product.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
        db.refresh(new_product)
        return new_product
    raise HTTPException(status_code=404, detail="Product not found")




@product_router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)) -> dict:
    product = db.query(Product).get(id)
    if product:
        db.delete(product)
        db.commit()
        return {
            "message": "product has been deleted"
        }
    raise HTTPException(status_code=404, detail="Product not found")
