from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from handbook import output_unit_data
from buildings_faculties import buildings_for_faculty

DATA_DIR = Path("data")
UNIT_LIST_PATH = DATA_DIR / "unit_list.txt"
UNIT_RAW_PATH = DATA_DIR/ "unit_raw.csv"
UNIT_TO_BUILDINGS_PATH = DATA_DIR/"unit_to_buildings.csv"
BUILDING_TO_UNITS_PATH = DATA_DIR/"building_to_units.csv"

def load_unit_list(path: Path) -> list[str]:
    with path.open() as f:
        return [line.strip().upper() for line in f if line.strip()]
    
def build_unit_metadata(unitcodes: list[str]) -> list[dict]:
    rows: list[dict] = []
    for code in unitcodes:
        print(f"=== Fetching {code} ===")
        meta = output_unit_data(code)
        if not meta:
            print(f"[warn] Skipping {code} (no metadata)")
            continue
        rows.append(meta)
    return rows

def infer_buildings_for_units(meta: dict) -> list[str]:
    # this would help us output likely buildings for where class could be
    faculty_buildings = buildings_for_faculty(meta.get("faculty") or "")
    seen = set()
    result = []
    for b in faculty_buildings:
        if b not in seen:
            seen.add(b)
            result.append(b)
    return result

def write_units_raw(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["unitcode", "unitname", "faculty", "discipline"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def write_unit_to_buildings(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["unitcode", "unitname", "building"]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for meta in rows:
            buildings = infer_buildings_for_units(meta)
            if not buildings:
                continue
            for b in buildings:
                writer.writerow(
                    {
                        "unitcode": meta["unitcode"],
                        "unitname": meta["unitname"],
                        "building": b,
                    }
                )
def write_buildings_to_units(unit_to_buildings_path: Path, output_path: Path) -> None:
    building_to_units: dict[str, list[dict]] = defaultdict(list)
    
    with unit_to_buildings_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            building = row["building"]
            building_to_units[building].append(
                {"unitcode": row["unitcode"], "unitname": row["unitname"]}
            )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["building", "unitcode", "unitname"]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for building, units in building_to_units.items():
            for u in units:
                writer.writerow(
                    {
                        "building": building,
                        "unitcode": u["unitcode"],
                        "unitname": u["unitname"],
                    }
                )
                
def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    unitcodes = load_unit_list(UNIT_LIST_PATH)
    print(f"Loaded {len(unitcodes)} unit codes from {UNIT_LIST_PATH}")

    #Scrape Handbook metadata
    meta_rows = build_unit_metadata(unitcodes)
    print(f"Got metadata for {len(meta_rows)} units")
    write_units_raw(meta_rows, UNIT_RAW_PATH)

    # Build unit to buildings
    write_unit_to_buildings(meta_rows, UNIT_TO_BUILDINGS_PATH)
    print(f"Wrote unit to buildings to {UNIT_TO_BUILDINGS_PATH}")

    # Build building to units
    write_buildings_to_units(UNIT_TO_BUILDINGS_PATH, BUILDING_TO_UNITS_PATH)
    print(f"Wrote building to units to {BUILDING_TO_UNITS_PATH}")


if __name__ == "__main__":
    main()
    