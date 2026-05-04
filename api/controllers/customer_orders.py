from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from ..dependencies.database import get_db
from api.models.orders import Order
from api.models.order_details import OrderDetail
from api.models.products import Product
from api.models.promotions import Promotion

router = APIRouter(
    prefix="/checkout",
    tags=["Customer Checkout"]
)


@router.post("/place-order")
def place_order(order_data: dict, db: Session = Depends(get_db)):
    order_type = order_data.get("order_type")
    if order_type not in ["takeout", "delivery"]:
        raise HTTPException(status_code=400, detail="Must specify 'takeout' or 'delivery'.")

    discount = 0.0
    promo_code = order_data.get("promo_code")
    if promo_code:
        promo = db.query(Promotion).filter(Promotion.code == promo_code, Promotion.is_active == True).first()
        if promo and promo.expiration_date > datetime.now():
            discount = promo.discount_percent

    running_total = 0.0
    order_items = []

    for item in order_data.get("items", []):
        product = db.query(Product).filter(Product.id == item["product_id"]).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item['product_id']} not found.")

        if product.stock_quantity < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}.")

        product.stock_quantity -= item["quantity"]

        item_total = product.price * item["quantity"]
        running_total += item_total
        order_items.append({"product_id": product.id, "quantity": item["quantity"], "price": product.price})

    final_total = running_total * (1 - discount)

    new_order = Order(
        user_id=None,
        total_price=final_total,
        order_type=order_type,
        status="received",
        tracking_number=str(uuid.uuid4())[:8].upper(),
        address=order_data.get("address") if order_type == "delivery" else "Pickup at Store"
    )

    db.add(new_order)
    db.flush()

    for item in order_items:
        detail = OrderDetail(
            order_id=new_order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["price"]
        )
        db.add(detail)

    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order placed successfully!",
        "tracking_number": new_order.tracking_number,
        "total_amount": round(new_order.total_price, 2)
    }