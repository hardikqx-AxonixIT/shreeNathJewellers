import json
import re
import time
from pathlib import Path

URL = "https://www.dwarikajewellers.com/"


def clean_rate(text: str):
    if not text:
        return None
    # extract digits and optional decimal
    m = re.search(r"[0-9,]+(?:\.[0-9]+)?", text.replace('\u00A0', ' '))
    if not m:
        return None
    num = m.group(0).replace(',', '')
    try:
        if '.' in num:
            return float(num)
        return int(num)
    except:
        return None


def write_rates(gold, silver):
    rates = {"gold": gold, "silver": silver}
    with open("rates.json", "w", encoding="utf-8") as f:
        json.dump(rates, f)
    print("Rates updated", rates)


def try_requests_bs4():
    try:
        import requests
        from bs4 import BeautifulSoup
    except Exception as e:
        print("requests/bs4 not available:", e)
        return False

    try:
        resp = requests.get(URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        gold_el = soup.find(id='price16')
        silver_el = soup.find(id='price18')
        gold = clean_rate(gold_el.get_text()) if gold_el else None
        silver = clean_rate(silver_el.get_text()) if silver_el else None
        if gold is not None and silver is not None:
            write_rates(gold, silver)
            return True
        print('Requests+BS4 did not find rates on page')
        return False
    except Exception as e:
        print('Requests error:', e)
        return False


def try_selenium():
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
    except Exception as e:
        print('Selenium or webdriver-manager not available:', e)
        return False

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        driver.get(URL)
        time.sleep(2)
        # try close popup
        try:
            driver.find_element(By.XPATH, "//button[contains(@class,'close')]").click()
        except:
            pass
        try:
            gold_text = driver.find_element(By.ID, 'price16').text
            silver_text = driver.find_element(By.ID, 'price18').text
            gold = clean_rate(gold_text)
            silver = clean_rate(silver_text)
            if gold is not None and silver is not None:
                write_rates(gold, silver)
                return True
        except Exception as e:
            print('Selenium element error:', e)
            return False
    finally:
        driver.quit()


if __name__ == '__main__':
    # Try fast request-based scrape first (works if server returns values in HTML)
    ok = try_requests_bs4()
    if not ok:
        print('Falling back to Selenium')
        ok = try_selenium()
    if not ok:
        print('Failed to update rates')
        # ensure rates.json exists with previous values or empty defaults
        p = Path('rates.json')
        if not p.exists():
            write_rates(None, None)