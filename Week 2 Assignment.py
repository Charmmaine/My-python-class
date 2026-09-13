import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import sys
 
# --- Config ---
BASE_URL = "https://books.toscrape.com/"
NUM_PRODUCTS = 12
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/GBP"
TARGET_CURRENCIES = ["USD", "KES"]
 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PriceScraperBot/1.0)"
}
 
 
def fetch_page(url):
    # Fetch a URL, handling connection errors gracefully
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Could not connect to {url}.")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request to {url} timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error for {url}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Unexpected request error: {e}")
    return None
 
 
def scrape_books(base_url, limit=10):
    # Scrape book name + price across pages until `limit` is reached
    products = []
    page_url = base_url
    page_num = 1
 
    while page_url and len(products) < limit:
        print(f"Scraping page {page_num}: {page_url}")
        html = fetch_page(page_url)
        if html is None:
            break
 
        soup = BeautifulSoup(html, "html.parser")
        book_cards = soup.select("article.product_pod")
 
        for card in book_cards:
            if len(products) >= limit:
                break
 
            # Get book name
            title_tag = card.h3.a
            name = title_tag["title"].strip() if title_tag else "Unknown"
 
            # Get and clean price
            price_tag = card.select_one("p.price_color")
            raw_price = price_tag.text.strip() if price_tag else "£0"
            cleaned_price = raw_price.replace("£", "").replace("Â", "").strip()
 
            try:
                price_gbp = float(cleaned_price)
            except ValueError:
                print(f"[WARN] Could not parse price for '{name}': '{raw_price}'")
                continue
 
            products.append({"product_name": name, "price_gbp": price_gbp})
 
        # Move to next page if one exists
        next_link = soup.select_one("li.next a")
        if next_link and len(products) < limit:
            page_url = base_url + next_link["href"]
            page_num += 1
            time.sleep(1)
        else:
            page_url = None
 
    return products
 
 
def get_exchange_rates(api_url, currencies):
    # Fetch current exchange rates for the target currencies
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
 
        if data.get("result") != "success":
            print("[ERROR] Exchange rate API did not return success.")
            return None
 
        rates = data.get("rates", {})
        return {cur: rates[cur] for cur in currencies if cur in rates}
 
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to the currency exchange API.")
    except requests.exceptions.Timeout:
        print("[ERROR] Currency exchange API request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Currency API error: {e}")
    except (KeyError, ValueError) as e:
        print(f"[ERROR] Unexpected response format from currency API: {e}")
 
    return None
 
 
def add_converted_prices(products, rates):
    # Add a price_<currency> field to each product
    if not rates:
        print("[WARN] No exchange rates available — only GBP prices will be saved.")
        return products
 
    for product in products:
        for currency, rate in rates.items():
            key = f"price_{currency.lower()}"
            product[key] = round(product["price_gbp"] * rate, 2)
 
    return products
 
 
def save_outputs(products, csv_path="products.csv", json_path="products.json"):
    # Save results to CSV and JSON
    if not products:
        print("[WARN] Nothing to save.")
        return
 
    fieldnames = list(products[0].keys())
 
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
 
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)
 
    print(f"\nSaved {len(products)} records to '{csv_path}' and '{json_path}'")
 
 
def display_table(products):
    # Print results as a formatted table
    if not products:
        print("[WARN] Nothing to display.")
        return
 
    headers = list(products[0].keys())
    rows = [list(p.values()) for p in products]
 
    try:
        from tabulate import tabulate
        print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))
    except ImportError:
        # Fallback if tabulate isn't installed
        col_widths = [
            max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
            for i, h in enumerate(headers)
        ]
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print("\n" + header_line)
        print("-" * len(header_line))
        for row in rows:
            print(" | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row)))
 
 
def main():
    print("Starting scrape...\n")
    products = scrape_books(BASE_URL, limit=NUM_PRODUCTS)
 
    if not products:
        print("[FATAL] No products were scraped. Exiting.")
        sys.exit(1)
 
    print(f"\nScraped {len(products)} products. Fetching exchange rates...")
    rates = get_exchange_rates(EXCHANGE_API_URL, TARGET_CURRENCIES)
 
    products = add_converted_prices(products, rates)
    display_table(products)
    save_outputs(products)
 
 
if __name__ == "__main__":
    main()
 