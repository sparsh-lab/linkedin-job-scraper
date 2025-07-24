import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os, json

# Load LinkedIn credentials from config file
with open("scr/config.json", "r") as f:
    config = json.load(f)
    username = config.get("username")
    password = config.get("password")

# start the Chrome
driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get('https://www.linkedin.com/')
time.sleep(2) 

with open("cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        # Remove 'sameSite' and 'expiry' if present, as Selenium may not accept them
        cookie.pop('sameSite', None)
        cookie.pop('expiry', None)
        driver.add_cookie(cookie)

# Save cookies AFTER you're logged in
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
print("✅ Cookies saved.")

driver.quit()