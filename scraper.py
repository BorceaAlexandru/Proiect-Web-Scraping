from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv
import xlwt
from xlwt import Workbook

def prelucrareDate(driver, game):
    print(game)
    list = []
    list.append(game)   #adaug id joc
    driver.get("https://steamdb.info/app/" + game + "/charts/") #accesez pag joc

    #time.sleep(1)

    #get variables
    gameName = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/div[1]/h1').get_attribute("innerHTML")
    #time.sleep(1)
    steamDBrating = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[2]/strong').get_attribute("innerHTML")[:-1]
    #time.sleep(1)
    positiveReviews = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[3]/strong').get_attribute("innerHTML")
    #time.sleep(1)
    negativeReviews = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[4]/strong').get_attribute("innerHTML")
    #time.sleep(1)
    followers = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[1]/ul/li[1]/strong').get_attribute("innerHTML")
    #time.sleep(1)
    peak24 = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[2]/ul/li[1]/strong').get_attribute("innerHTML")
    #time.sleep(1)
    peakalltime = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[2]/ul/li[3]/strong').get_attribute("innerHTML")

    list.append(gameName)
    list.append(steamDBrating)
    list.append(positiveReviews)
    list.append(negativeReviews)
    list.append(followers)
    list.append(peak24)
    list.append(peakalltime)

    time.sleep(6)
    #time.sleep(2)
    driver.back()

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
    gamesID = []
    for game in games:
        gamesID.append(game.get_attribute("data-appid"))

    #vreau sa bag datele intr un excel
    wb=xlwt.Workbook()

    #adaug sheet
    sheet1 = wb.add_sheet("Sheet1", cell_overwrite_ok=False)

    list_final = []
    #f=open("games.csv", "w")
    #writer=csv.writer(f)
    i=0
    for game in gamesID:

        list_final.append(prelucrareDate(driver, game))
        #writer.writerows(prelucrareDate(driver, game))
        """
        list_final.append(prelucrareDate(driver, game))
        sheet1.write(i+1, 1, list_final[i])
        i=i+1
        """

    print(list_final)
    #wb.save("xlwt GameData.xlsx")
    #f.close()
