from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..dependencies.database import get_db
from ..models.payments import Payment
from ..models.orders import Order
from ..schemas.payments import PaymentCreate, PaymentRead, PaymentUpdate

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(request: PaymentCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_payment = Payment(
        order_id=request.order_id,
        method=request.method,
        status=request.status,
        amount=request.amount,
        created_at=datetime.now()
    )

    if request.status.lower() in ["completed", "paid", "success"]:
        order.status = "Paid"

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    return payment


@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: int, request: PaymentUpdate, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


@router.get("/order/{order_id}", response_model=list[PaymentRead])
def get_order_payments(order_id: int, db: Session = Depends(get_db)):
    return db.query(Payment).filter(Payment.order_id == order_id).all()