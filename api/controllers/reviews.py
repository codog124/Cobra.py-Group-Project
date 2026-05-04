from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..dependencies.database import get_db
from ..models.reviews import Review
from ..schemas.reviews import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews & Feedback"]
)


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(request: ReviewCreate, db: Session = Depends(get_db)):

    new_review = Review(
        user_id=request.user_id,
        menu_item_id=request.menu_item_id,
        rating=request.rating,
        comment=request.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/", response_model=List[ReviewRead])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.get("/menu-item/{menu_item_id}", response_model=List[ReviewRead])
def get_reviews_by_item(menu_item_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.menu_item_id == menu_item_id).all()


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, request: ReviewUpdate, db: Session = Depends(get_db)):
    review_query = db.query(Review).filter(Review.id == review_id)
    review = review_query.first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    update_data = request.model_dump(exclude_unset=True)
    review_query.update(update_data)

    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return None