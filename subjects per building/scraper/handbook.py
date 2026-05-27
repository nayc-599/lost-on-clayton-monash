import requests
from bs4 import BeautifulSoup

# handbook url
sample_url = "https://handbook.monash.edu/2026/units/{UNITCODE}?year=2026"


def fetch_unit_metadata(unitcode: str) -> dict|None:
    # we want unitcode and unitname from the monash handbook. it returns non if the page is missing
    url = sample_url.format(UNITCODE=unitcode.upper())
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        print("[handbook] {unitcode}: HTTP {resp.status_code}")
        return None
    
    soup = BeautifulSoup(resp.text, "html.parser")  # html parser
    # parsing for unitcode
    # <title> FIT1058 - Foundations of computing - Monash Univeristy </title>
    h1 = soup.title.string()
    #if can't find the unit code
    if not h1 or not h1.text.strip():
        print(f"[handbook] {unitcode}: could not find <h1>")
        return None
    # title of the unit/unitname
    title = h1.text.strip()
    # <title> FIT1058 - Foundations of computing - Monash Univeristy </title>
    parts = title.split(" ",1)
    unitcode, unitname = parts[0].upper(), parts[1].strip()
    
    return {
        "unitcode": unitcode,
        "unitname": unitname,
    }
    