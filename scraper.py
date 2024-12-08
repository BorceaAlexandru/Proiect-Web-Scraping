from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def principal():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get("https://steamdb.info/stats/globaltopsellers/?displayOnly=Game")

    dropdown = driver.find_element(By.XPATH, '//*[@id="dt-length-0"]')
    select = Select(dropdown)
    select.select_by_value("1000")

    meniu = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody')
    games = meniu.find_elements(By.CSS_SELECTOR, "tr")
    i=0
    list =[]
    for game in games:
        i=i+1
        list.append(game.get_attribute("data-appid"))
        #print(game.get_attribute("data-appid"))
    #current_track = track.get_attribute("aria-rowindex")
    print(list)
