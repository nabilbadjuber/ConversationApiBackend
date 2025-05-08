from sqlalchemy import Column, Integer, String
from app.database import Base

class Scenario(Base):
    __tablename__ = "scenario"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    imageurl = Column(String)
    role = Column(String)
    place = Column(String)
