from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

chrome_options = Options()
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.dwarikajewellers.com/")
time.sleep(1)

gold = driver.find_element(By.ID, "price16").text

# Scroll page
driver.execute_script("window.scrollBy(0,500);")
time.sleep(1)

# Close popup if present
try:
    driver.find_element(By.XPATH, "//button[contains(@class,'close')]").click()
    print("Popup closed")
except:
    print("Popup not found")

silver = driver.find_element(By.ID, "price18").text

print("Gold Rate:", gold)
print("Silver Rate:", silver)

rates = {
    "gold": gold,
    "silver": silver
}

with open("rates.json", "w") as f:
    json.dump(rates, f)

print("Rates updated")

driver.quit()