from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from ..dependencies.database import get_db
from api.models.promotions import Promotion

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions & Discount Management"]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_promo_code(promo_in: dict, db: Session = Depends(get_db)):
    existing = db.query(Promotion).filter(Promotion.code == promo_in['code']).first()
    if existing:
        raise HTTPException(status_code=400, detail="Promo code already exists")

    new_promo = Promotion(**promo_in)
    db.add(new_promo)
    db.commit()
    db.refresh(new_promo)
    return new_promo


@router.get("/")
def list_all_promos(db: Session = Depends(get_db)):
    return db.query(Promotion).all()


@router.delete("/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    promo = db.query(Promotion).filter(Promotion.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")

    db.delete(promo)
    db.commit()
    return {"message": "Promotion deleted successfully"}



@router.get("/validate/{code}")
def validate_promo(code: str, db: Session = Depends(get_db)):
    promo = db.query(Promotion).filter(
        Promotion.code == code,
        Promotion.is_active == True
    ).first()

    if not promo:
        raise HTTPException(status_code=404, detail="Invalid promo code")

    if promo.expiration_date < datetime.now():
        raise HTTPException(status_code=400, detail="This promo code has expired")

    return {
        "code": promo.code,
        "discount_percent": promo.discount_percent,
        "message": "Promo code applied successfully!"
    }