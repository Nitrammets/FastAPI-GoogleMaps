from sqlalchemy import Column, String, Integer, Sequence, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self) -> str:
        return f"{self.name}"

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    def __repr__(self):
        return f"{self.url}"

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(String, unique=True)
    name = Column(String)
    rating = Column(Float)
    address = Column(String)
    price_level = Column(Integer)
    categories = relationship("Category", secondary="business_categories")
    photos = relationship("Photo", secondary="business_photos")

class BusinessCategory(Base):
    __tablename__ = "business_categories"
    business_id = Column(Integer, ForeignKey("businesses.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)

class BusinessPhotos(Base):
    __tablename__ = "business_photos"
    business_id = Column(Integer, ForeignKey("businesses.id"), primary_key=True)
    photo_id = Column(Integer, ForeignKey("photos.id"), primary_key=True)