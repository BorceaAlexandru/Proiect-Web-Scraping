from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def principal():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get("https://steamdb.info/stats/globaltopsellers/")
    time.sleep(10)
