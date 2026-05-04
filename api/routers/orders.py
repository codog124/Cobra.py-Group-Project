from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..controllers import order_tracking as tracking_controller # New Import
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.get("/track/{tracking_number}", response_model=schema.Order)
def track(tracking_number: str, db: Session = Depends(get_db)):
    return tracking_controller.track_order_by_id(db, tracking_number)

@router.get("/search", response_model=list[schema.Order])
def search(query: str, db: Session = Depends(get_db)):
    return tracking_controller.advanced_order_search(db, query)





@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)