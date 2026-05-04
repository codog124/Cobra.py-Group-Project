from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..dependencies.database import get_db
from ..models.products import Product


router = APIRouter(
    prefix="/products",
    tags=["Products/Menu Management"]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_menu_item(product_in: dict, db: Session = Depends(get_db)):
    new_product = Product(**product_in)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/{product_id}")
def update_menu_item(product_id: int, updates: dict, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updates.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_menu_item(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_active = False
    db.commit()
    return {"message": f"Product {product_id} has been deactivated from the menu"}



@router.get("/low-stock")
def get_low_stock_alerts(threshold: int = 10, db: Session = Depends(get_db)):
    low_stock_items = db.query(Product).filter(
        Product.stock_quantity <= threshold,
        Product.is_active == True
    ).all()
    return low_stock_items


# --- CUSTOMER PERSPECTIVE: SEARCH & VIEW ---

@router.get("/", response_model=List[dict])
def get_all_menu_items(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()


@router.get("/search")
def search_menu(query: str, db: Session = Depends(get_db)):
    results = db.query(Product).filter(
        (Product.name.contains(query)) | (Product.description.contains(query)),
        Product.is_active == True
    ).all()
    return results


@router.get("/{product_id}")
def get_product_details(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product