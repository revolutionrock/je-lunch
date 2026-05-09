import requests
import json
import csv
from datetime import date

GRAPHQL_URL = "https://api.schoolnutritionandfitness.com/graphql"
MENU_ID = "69c57eef1362d4403e38d8c6"
SITE_CODE = "27928"

# Month is 0-indexed in their system (4 = May)
MONTH = 4
YEAR = 2026

HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://www.schoolnutritionandfitness.com",
    "Referer": "https://www.schoolnutritionandfitness.com/",
    "User-Agent": "Mozilla/5.0",
}

QUERY = """
{
    menu(id:"%s") {
        id
        month
        year
        items {
            day
            product {
                id
                name
                category
                portion_size
                prod_calories
                prod_protein
                prod_carbs
                prod_total_fat
                prod_sodium
                prod_calcium
                prod_iron
                prod_dietary_fiber
                prod_sugar: sugar
                allergen_milk
                allergen_wheat
                allergen_soy
                allergen_egg
                allergen_fish
                allergen_peanut
                allergen_treenuts
                allergen_sesame
                allergen_gluten
                allergen_vegetarian
                prod_allergens
            }
        }
    }
}
""" % MENU_ID

def fetch_menu():
    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={"query": QUERY}
    )
    response.raise_for_status()
    return response.json()

def parse_to_csv(data, output_file="menu.csv"):
    items = data["data"]["menu"]["items"]
    month = data["data"]["menu"]["month"]
    year = data["data"]["menu"]["year"]

    rows = []
    for item in items:
        day = item["day"]
        p = item["product"]
        if not p:
            continue

        # Build a real date (month is 0-indexed)
        try:
            dt = date(year, month + 1, day)
            date_str = dt.strftime("%Y-%m-%d")
            weekday = dt.strftime("%A")
        except ValueError:
            date_str = f"{year}-{month+1:02d}-{day:02d}"
            weekday = ""

        allergens = []
        for field in ["allergen_milk","allergen_wheat","allergen_soy","allergen_egg",
                      "allergen_fish","allergen_peanut","allergen_treenuts",
                      "allergen_sesame","allergen_gluten"]:
            if p.get(field) == "1":
                allergens.append(field.replace("allergen_",""))

        rows.append({
            "date": date_str,
            "weekday": weekday,
            "day": day,
            "category": p.get("category",""),
            "name": p.get("name",""),
            "portion_size": p.get("portion_size",""),
            "calories": p.get("prod_calories",""),
            "protein_g": p.get("prod_protein",""),
            "carbs_g": p.get("prod_carbs",""),
            "fat_g": p.get("prod_total_fat",""),
            "sodium_mg": p.get("prod_sodium",""),
            "fiber_g": p.get("prod_dietary_fiber",""),
            "calcium_mg": p.get("prod_calcium",""),
            "iron_mg": p.get("prod_iron",""),
            "allergens": ", ".join(allergens),
            "vegetarian": "yes" if p.get("allergen_vegetarian") == "1" else "",
        })

    rows.sort(key=lambda r: (r["day"], r["category"], r["name"]))

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} items to {output_file}")

if __name__ == "__main__":
    data = fetch_menu()
    parse_to_csv(data)