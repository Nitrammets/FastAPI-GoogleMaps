from fastapi import FastAPI, HTTPException, Depends, Response
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MapsAPI.models import Base, Business, Photo, Category
from MapsAPI.main import Scraper

app = FastAPI()

def get_db():
    engine = create_engine('sqlite:///./businesses.db')
    session = sessionmaker(bind=engine)()
    return session

@app.get("/business/{business_id}/categories")
def read_categories(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return business.categories

@app.get("/business/all")
def get_details(db: Session = Depends(get_db)):
    business = db.query(Business).all()
    return business

@app.post("/generate-data/{query}")
def generate_data(query: str, db:Session = Depends(get_db)):
    scraper = Scraper()
    scraper.scrape(query)
    return Response(content="Scraped", status_code=202)

