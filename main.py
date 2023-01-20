from fastapi import FastAPI, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from MapsAPI.models import Base, Business, Photo, Category
from MapsAPI.main import Scraper
import logging

app = FastAPI(debug=True)

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
def get_all(db: Session = Depends(get_db)):
    business = db.query(Business).all()
    return business

@app.get("/get-business/{business_id}")
def get_details( business_id: int, db: Session = Depends(get_db),):
    business = db.query(Business).options(joinedload(Business.categories), joinedload(Business.photos)).get(business_id)
    return business

@app.get("/get-slugs/all")
def get_slugs(db: Session=Depends(get_db)):
    slugs = db.query(Business.slug).all()
    return slugs

@app.post("/generate-data/")
def generate_data(request_data: dict, db:Session = Depends(get_db)):
    scraper = Scraper()
    scraper.scrape(request_data.get("query", ""))
    return Response(content="Scraped", status_code=202)

@app.get("/get-business-by-slug/{slug}")
def get_business_by_slug(slug: str, db:Session=Depends(get_db)):
    businesses = db.query(Business).options(joinedload(Business.categories), joinedload(Business.photos)).filter_by(slug=slug).all()
    print(businesses)
    return businesses
