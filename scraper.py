from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv

def prelucrareDate(driver, game):
    list = []
    list.append(game.get_attribute("data-appid"))   #adaug id joc
    driver.get("https://steamdb.info/app/" + game.get_attribute("data-appid") + "/charts/") #accesez pag joc

    #get variables
    gameName = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/div[1]/h1').get_attribute("innerHTML")
    steamDBrating = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[2]/strong').get_attribute("innerHTML")[:-1]
    positiveReviews = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[3]/strong').get_attribute("innerHTML")
    negativeReviews = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[4]/strong').get_attribute("innerHTML")
    followers = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[1]/ul/li[1]/strong').get_attribute("innerHTML")
    peak24 = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[2]/ul/li[1]/strong').get_attribute("innerHTML")
    peakalltime = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[2]/ul/li[3]/strong').get_attribute("innerHTML")

    list.append(gameName)
    list.append(steamDBrating)
    list.append(positiveReviews)
    list.append(negativeReviews)
    list.append(followers)
    list.append(peak24)
    list.append(peakalltime)

    #driver.back()

    return list



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

    list_final = []
    #f=open("games.csv", "w")
    #writer=csv.writer(f)
    for game in games:
        list_final.append(prelucrareDate(driver, game))
        #writer.writerows(prelucrareDate(driver, game))

    print(list_final)

    #f.close()