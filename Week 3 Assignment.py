import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import sys

BASE_URL= "https://books.toscrape.com/"
NUM_PRODUCTS = 12
EXCHANGE_API_URL = "https://opem.er-api.com/v6/latest/GBP"
TARGET_CURRENCIES =["USD","KES"]

HEADERS= {"User-Agent:Mozilla/5.0 (compatible; PriceScraperBot/1.0)"}

def fetch_page(url):
    """
    Fetch a URL with error handling for connection issues,
    timeouts, and bad HTTP status codes.
    """
    try:
        response = requests.get(url,headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Could not connect to{url} Check your internet connection")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request to {url} timed out.")
    except requests.exceptions.HTTPError:
        print(f"[ERROR] HTTP error for {url}:")
    except requests.exceptions.RequestException:
        print(f"[ERROR] Unexpected request error:")
    return None

def scrape_books(base_url, limit=10):
     """
    Scrapes book titles and prices from books.toscrape.com.
    Walks across pages until `limit` products are collected.
    """
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
            title_tag = card.h3.a
            name = title_tag["title"].strip() if title_tag else "Unknown"

            price_tag = card.select_one("p.price_color")
            raw_price = price_tag.text.strip() if price_tag else "£0"


            cleaned_price = (
                raw_price.replace("£", "")
                .replace("Â", "")
                .strip()
                 )
            try:
                price_gbp = float(cleaned_price)
            except ValueError:
                print(f"[WARN] Could not parse price for '{name}': '{raw_price}'")
                continue
 
            products.append({"product_name": name, "price_gbp": price_gbp})
        next_link = soup.select_one("li.next a")
        if next_link and len(products) < limit:
            page_url = base_url + next_link["href"]
            page_num += 1
            time.sleep(1)  # be polite, don't hammer the server
        else:
            page_url = None
 
    return products
 
def get_exchange_rates(api_url, currencies):
    """
    Fetches current exchange rates with GBP as the base currency.
    Returns a dict like {"USD": 1.27, "KES": 164.5} or None on failure.
    """
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
    """
    Takes the list of {"product_name": ..., "price_gbp": ...} dicts
    and adds a price_<currency> key for each target currency.
    Works in place on plain Python dicts/lists — no pandas needed.
    """
    if not rates:
        print("[WARN] No exchange rates available — only GBP prices will be saved.")
        return products
 
    for product in products:
        for currency, rate in rates.items():
            key = f"price_{currency.lower()}"
            product[key] = round(product["price_gbp"] * rate, 2)
 
    return products