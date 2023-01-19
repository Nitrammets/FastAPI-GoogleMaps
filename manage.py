from MapsAPI.main import Scraper
import argparse

parser = argparse.ArgumentParser(description="Scrape Google Maps API listings")
parser.add_argument('query', type=str, help="searchterm")


if __name__ == '__main__':
    args = parser.parse_args()
    scraper = Scraper()
    scraper.scrape(query=args.query)
    scraper.session.commit()