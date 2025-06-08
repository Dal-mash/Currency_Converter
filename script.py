from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import requests
from selenium.webdriver.edge.service import Service
import time
import random



def run():
    service = Service("D:/SOFTWARE/msedgedriver.exe")
    driver = webdriver.Edge(service=service)
    wait = WebDriverWait(driver, 30)

    converted_list = []
    currency_list = list(set(["USD", "JPY", "CAD", "EUR", "GBP", "CHF", "AUD", "NZD", "CNY", 
                              "INR", "RUB", "BRL", "ZAR", "MXN", "SGD", "HKD", "SEK", "NOK", 
                              "DKK", "TRY", "KRW", "IDR", "THB", "MYR", "PHP", "VND", "ILS", 
                              "SAR", "AED", "QAR", "KWD", "BHD", "OMR", "EGP", "PKR", "LKR", 
                              "NGN", "TWD", "CZK", "HUF", "PLN", "ARS", "COP", "PEN", "RON", 
                              "MAD", "UYU", "KES", "GHS", "BDT", "UAH"]))

    try:
        print("Starting currency conversion...")
        for currency in currency_list:
            print(f"Converting {currency} to USD...")
            driver.get(f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={currency}&To=USD")
            time.sleep(random.uniform(2, 4))
            try:
                print("Waiting for the conversion result to load...")
                val = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'sc-708e65be-1')]"))
                ).text
                print(f"Conversion result for {currency}: {val}")
                val = val.split(" ")[0].replace(",", "")
                val = float(val)
                converted_list.append({currency: val})

                print(f"Converted {currency} to USD: {val}")
            except (NoSuchElementException, TimeoutException):
                continue
        print("Currency conversion completed successfully.")
    finally:
        print("Closing the browser...")
        driver.quit()
    
    return converted_list

converted_list = run()

url = "http://localhost:3000/update-json"
res = requests.post(url, json=converted_list, headers={"Content-Type": "application/json"})
print(res.status_code)



