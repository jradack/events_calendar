from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

# Define class for a site
class Site:
    def __init__(self, name, url, selectors):
        self.name = name
        self.url = url
        self.selectors = selectors
        self.req = Request(url = self.url, headers={'User-Agent': 'Mozilla/5.0'})

    def __str__(self):
        return f"{self.name}"

    
    def requestSite(self):
        '''Request site for the page'''
        page = urlopen(self.req).read()
        soup = BeautifulSoup(page, "html.parser")
        page_selectors = self.selectors["page"]
        return(soup.find_all(page_selectors[0], class_=page_selectors[2]))

    def getInfo():
        pass

# Define class for scraped content
class ScrapedContent:
    def __init__(self, site):
        self.site = site
        self.request_results = site.requestSite()
        self.contents = None
    
    def getContents(self):
        pass


# Print out info of page results
def getInfo(results, content_selector):
    '''Process info from a page request'''
    for element in results:
        for key, val in content_selector.items():
            # Skip if selector is missing
            if val is None:
                continue
            # Process field
            if val[1] == "id":
                entry = element.find(val[0], id=re.compile(val[2]))
            elif val[1] == "class":
                entry = element.find(val[0], class_=re.compile(val[2]))
            if entry is not None:
                print(entry.text.strip())
            else:
                print(key + ": Missing")
        print()


# Run
if __name__ == "__main__":
    page_dat = [
        # Union Transfer
        {
            "name": "Union Transfer",
            "url": "https://utphilly.com/events/",
            "selectors": {
                "page": ["div", "id", "eventWrapper"],
                "contents": {
                    "date": ["div", "id", "eventDate"],
                    "tagline": ["div", "class", "event_tagline"],
                    "name": ["a", "id", "eventTitle"],
                    "venue": ["a", "id", "venueLink"],
                    "age_restriction": ["div", "class", "eventAgeRestriction"],
                    "door_time": ["div", "class", "eventDateDetails"],
                    "cost": ["div", "class", "eventCost"]
                }
            }
        },
        # Mann Center
        {
            "name": "The Mann Center",
            "url": "https://manncenter.org/events",
            "selectors": {
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
        },
        # Underground Arts
        {
            "name": "Underground Arts",
            "url": "https://undergroundarts.org/",
            "selectors": {
                "page": ["article", "class", "list-view-item"],
                "contents": {
                    "date": ["div", "class", "detail_event_date"],
                    "name": ["h1", "class", "event-name"],
                    "subtitle": ["div", "class", "detail_event_subtitle"],
                    "door_time": ["div", "class", "detail_door_time"],
                    "event_time": ["div", "class", "detail_event_time"]
                }
            }
        }
    ]
    
    union_transfer = Site(page_dat[2]["name"], page_dat[2]["url"], page_dat[2]["selectors"])
    print(union_transfer)

    request_result = union_transfer.requestSite()
    print("Length of list: " +  str(len(request_result)))

    getInfo(request_result, union_transfer.selectors['contents'])





