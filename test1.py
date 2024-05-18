from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True  # Run Chrome in headless mode
options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
options.add_argument("--no-sandbox")  # Required for running on some systems
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

driver = webdriver.Chrome(options=options)

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
