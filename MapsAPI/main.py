import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import time
from .models import Base, Business, Photo, Category
from datetime import datetime, date

def generate_slug(name: str, address: str) -> str:
    name_list = name.split(" ")
    address_list = address.split(" ")[:2]
    adress_slug = "-".join(address_list)
    final_str = "-".join(name_list) + "-" + f"{adress_slug}"
    return final_str.replace("ö", "o").replace("ä", "a").replace("ü","u").replace("õ","o")


class Scraper:
    def __init__(self) -> None:
        self.base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        self.api_key = ""
        self.engine = create_engine('sqlite:///./businesses.db')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
    
    def get_categories_by_business_id(self, id):
        business = self.session.query(Business).filter_by(id=id).first()
        return business.categories
    
    def get_photos_by_business_id(self, id):
        business = self.session.query(Business).filter_by(id=id).first()
        return business.photos
    
    def scrape(self, query: str, fields: list = None):
        if len(query) == 0:
            return
        formatted_query = "%20".join(query.split(" "))
        #formatted_fields = ",".join(fields)
        url = f"{self.base_url}&query={formatted_query}&key={self.api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        i = 0
        while True:
            print(f"{i}nth page")
            for place in data["results"]:
                existing_business = self.session.query(Business).filter_by(place_id=place["place_id"]).scalar()
                if existing_business is None:
                    business = Business(
                        name=place["name"],
                        rating=place.get("rating", None),
                        address=place["formatted_address"],
                        price_level=place.get("price_level", None),
                        place_id=place.get("place_id"),
                        slug=generate_slug(place["name"],place["formatted_address"]).lower()
                    )
                    for category in place.get("types", []):
                        existing_category = self.session.query(Category).filter_by(name=category).scalar()
                        if existing_category is None:
                            new_category = Category(name=category)
                            self.session.add(new_category)
                            business.categories.append(new_category)
                        else:
                            business.categories.append(existing_category)
                    for photo in place.get("photos", []):
                        new_photo = Photo(
                            url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key={self.api_key}"
                        )
                        self.session.add(new_photo)
                        business.photos.append(new_photo)
                    self.session.add(business)           
            next_page_token = data.get("next_page_token", None)
            if not next_page_token:
                break
            time.sleep(2)
            i+=1
            url = f"{self.base_url}pagetoken={next_page_token}&key={self.api_key}"
            response = requests.get(url)
            data = json.loads(response.text)
        self.session.commit()
        return True






