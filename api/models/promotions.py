from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True)
    discount_percent = Column(Float)
    expiration_date = Column(DateTime)
    active = Column(Boolean, default=True)
