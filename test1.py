import os  # Import the os module

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Chrome options for running on Heroku
options = Options()
options.headless = True
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Specify the path to the ChromeDriver
chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
chrome_driver_path = os.environ.get("CHROMEDRIVER_PATH", "/app/.chromedriver/bin/chromedriver")

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get('https://app.magmail.eu.org/get_keys')
    time.sleep(5)  # Adjust the sleep time if necessary to allow the page to load
    input_element = driver.find_element_by_name('link')
    input_element.send_keys('https://cpvod.testbook.com/659ba2ba1ffd3734c48d6498/playlist.m3u8')
    input_element.submit()
    time.sleep(5)  # Wait for the form submission to complete
    response = driver.page_source
    print(response)
finally:
    driver.quit()
