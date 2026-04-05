from sqlalchemy import Column, Integer, String, Float
from ..dependencies.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Float)
    unit = Column(String)
