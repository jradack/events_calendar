from django.core.management.base import BaseCommand

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime

class Site:
    """Defines class for a website and requesting"""
    def __init__(self, name, url, selectors):
        self.name = name
        self.url = url
        self.selectors = selectors
        self.req = Request(url = self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.raw_content = None

    def __str__(self):
        return f"{self.name}"
    
    def requestSite(self):
        '''Request site for the page'''
        page = urlopen(self.req).read()
        soup = BeautifulSoup(page, "html.parser")
        page_selectors = self.selectors["page"]
        self.raw_content = soup.find_all(page_selectors[0], class_=page_selectors[2])


def process_field(element, selector_key, selector_val):
    """Function for processing a single field"""
    # Skip if selector is missing
    if selector_val is None:
        return None
    # Process field
    if selector_val[1] == "id":
        entry = element.find(selector_val[0], id=re.compile(selector_val[2]))
    elif selector_val[1] == "class":
        entry = element.find(selector_val[0], class_=re.compile(selector_val[2]))
    # Return result
    # if entry == None:
    #     return None
    # match selector_key:
    #     case "event_link":
    #         return entry["href"]
    #     case "thumbnail_image":
    #         return entry["src"]
    #     case _:
    #         return entry.text.strip() 
    if selector_val[0] == "a":
        if selector_val[3]:
            return entry["href"]
    if selector_val[0] == "img":
        return entry["src"]
    if entry is not None:
        return entry.text.strip()
    return None

def fetch_union_transfer_events():
    """Fetches events for Union Transfer"""
    # Define parameters
    name = "Union Transfer"
    url= "https://utphilly.com/events/"
    selectors = {
        "page": ["div", "id", "eventWrapper"],
        "contents": {
            "name": ["a", "id", "eventTitle", False],
            "date": ["div", "id", "eventDate"],
            "cost": ["div", "class", "eventCost"],
            "door_time": ["div", "class", "eventDateDetails"],
            "age_restriction": ["div", "class", "eventAgeRestriction"],
            "tagline": ["div", "class", "eventTagLine"],
            "event_link": ["a", "id", "eventTitle", True],
            "stage": ["a", "class", "venueLink", False],
            "thumbnail_image": ["img", "class", "eventListImage"]
        }
    }

    # Create site object
    union_transfer = Site(name, url, selectors)
    union_transfer.requestSite()
    # print(union_transfer.raw_content)
    for element in union_transfer.raw_content:
        scraped_data = {k: process_field(element, k, v) for k, v in selectors["contents"].items()}
        
        # Date
        for long_name, short_name in {"June":"Jun", "July":"Jul", "Sept":"Sep"}.items():
            scraped_data["date"] = scraped_data["date"].replace(long_name, short_name)
        scraped_data["date"] =  datetime.strptime(scraped_data['date'], "%a, %b %d").replace(year = 2023)

        # Door/show time
        # Cost
        print(scraped_data)

def fetch_mann_center_events():
    """Fetches events for the Mann Center"""
    name = "The Mann Center",
    url = "https://manncenter.org/events",
    selectors = {
        "page": ["div", "class", "views-row"],
        "contents": {
            "date": ["div", "class", "event-date"],
            "tagline": None,
            "name": ["div", "class", "display-title"],
            "subtitle": ["div", "class", "subtitle"],
            "venue": ["a", "id", "event-type"],
            "age_restriction": None,
            "door_time": None,
            "cost": None
        }
    }

def fetch_underground_arts():
    """Fetches events for Underground Arts"""
    name = "Underground Arts",
    url = "https://undergroundarts.org/",
    selectors = {
        "page": ["article", "class", "list-view-item"],
        "contents": {
            "date": ["div", "class", "detail_event_date"],
            "name": ["h1", "class", "event-name"],
            "subtitle": ["div", "class", "detail_event_subtitle"],
            "door_time": ["div", "class", "detail_door_time"],
            "event_time": ["div", "class", "detail_event_time"]
        }
    }

class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch_union_transfer_events()