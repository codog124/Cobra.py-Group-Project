from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..dependencies.database import get_db
from ..models.orders import Order
from ..schemas import orders as schema

router = APIRouter(
    prefix="/tracking",
    tags=["Order Tracking & Search"]
)

@router.get("/{tracking_number}", response_model=schema.Order)
def track_order_by_id(tracking_number: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.tracking_number == tracking_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Tracking number not found")
    return order

@router.get("/search/", response_model=list[schema.Order])
def advanced_order_search(query: str, db: Session = Depends(get_db)):
    results = db.query(Order).filter(
        or_(
            Order.guest_name.ilike(f"%{query}%"),
            Order.tracking_number.ilike(f"%{query}%"),
            Order.guest_phone.ilike(f"%{query}%")
        )
    ).all()
    return results
