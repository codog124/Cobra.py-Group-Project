from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date
from typing import List
from ..dependencies.database import get_db
from ..models.orders import Order
from ..models.order_items import OrderItem
from ..models.products import Product
from ..models.reviews import Review

router = APIRouter(
    prefix="/analytics",
    tags=["Restaurant Analytics & Reporting"]
)



@router.get("/revenue/daily")
def get_daily_revenue(target_date: date, db: Session = Depends(get_db)):
    revenue = db.query(func.sum(Order.total_price)).filter(
        func.date(Order.created_at) == target_date,
        Order.status != "cancelled"
    ).scalar()

    return {
        "date": target_date,
        "total_revenue": revenue or 0.0
    }



@router.get("/dishes/performance")
def get_dish_performance(limit: int = 5, db: Session = Depends(get_db)):
    performance = db.query(
        Product.name,
        func.count(OrderItem.id).label("total_sales")
    ).join(OrderItem, Product.id == OrderItem.product_id, isouter=True) \
        .group_by(Product.id) \
        .order_by("total_sales") \
        .limit(limit).all()

    return [{"product": p.name, "sales_count": p.total_sales} for p in performance]



@router.get("/dishes/complaints")
def get_dish_complaints(db: Session = Depends(get_db)):
    complaints = db.query(
        Product.name,
        func.avg(Review.rating).label("average_rating"),
        func.group_concat(Review.comment).label("comments")
    ).join(Review, Product.id == Review.product_id) \
        .group_by(Product.id) \
        .having(func.avg(Review.rating) <= 3.0) \
        .order_by(func.avg(Review.rating)).all()

    return [
        {
            "product": c.name,
            "average_rating": round(c.average_rating, 2),
            "feedback_summary": c.comments.split(",") if c.comments else []
        } for c in complaints
    ]