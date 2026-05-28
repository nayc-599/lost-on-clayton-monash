from __future__ import annotations

import requests
from bs4 import BeautifulSoup

# handbook url
sample_url = "https://handbook.monash.edu/2026/units/{UNITCODE}?year=2026"

# we want the page for the unit
def fetch_unit_page(unitcode: str) -> BeautifulSoup|None:
    url = sample_url.format(UNITCODE=unitcode.upper())
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        print(f"[handbook] {unitcode}: HTTP {resp.status_code}")
        return None
    return BeautifulSoup(resp.text, "htmp.parser")

# extracting unitname, unitcode, faculty from the Handbook page
def parse_unit(soup: BeautifulSoup, unitcode: str) -> dict | None:
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
    if len(parts) != 2:
        print(f"[handbook] {unitcode}: unexpected title format {title!r}")
        unitname = title
    else:
        unitname = parts[1].strip()
    
# Faculty: extracting the faculty from the html script
def find_faculty(soup: BeautifulSoup) -> Optional[str]:
    # need to find a heading that starts with "Faculty: "
    faculty_heading = soup.find(
        ["h3", "h4"],
        string = lambda t: isinstance(t, str) and t.strip().startswith("Faculty:"),
    )
    if not faculty_heading:
        return None
    # the faculty name is given in a link
    link = faculty_heading.find_next("a")
    if link and link.get_text(strip=True):
        text = link.get_text(strip=True)
        return text.replace("Faculty of ", "").strip()
    return None

def output_unit_data(unitcode: str) -> Optional[Dict[str, str]]:
    # returns a dictionary with the: unitcode, unitname and faculty
    unitcode = unitcode.upper()
    soup = fetch_unit_page(unitcode)
    if soup is None:
        return None
    
    unitname = parse_unit(soup, unitcode)
    if not unitname:
        print(f"[handbook] {unitcode}: could not parse unit title")
        return None
    
    faculty = find_faculty(soup)
    return {
        "unitname": unitcode,
        "unitname": unitname,
        "faculty": faculty or "",
    }

if __name__ == "__main__":
    meta = output_unit_data("FIT1058")
    print(meta)