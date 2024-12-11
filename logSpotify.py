from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from scraper import *

def playlistCreation(df, name):
    driver = setDriver()
    driver.get('https://accounts.spotify.com/en/login')

    username = driver.find_element(By.XPATH, '//*[@id="login-username"]')
    password = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    submit = driver.find_element(By.XPATH, '//*[@id="login-button"]')

    username.send_keys("mikeholera43@gmail.com")
    password.send_keys("SalutColegi1")
    time.sleep(1)
    submit.click()

    webPlayer = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/button[2]')
    webPlayer.click()
    time.sleep(1)

    acceptCookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    acceptCookies.click()
    createPlaylist = driver.find_element(By.XPATH, '//*[@id="Desktop_LeftSidebar_Id"]/nav/div/div[1]/div[1]/header/div/span/button')
    createPlaylist.click()
    newPlaylist = driver.find_element(By.XPATH, '//*[@id="context-menu"]/ul/li[1]/button')
    newPlaylist.click()

    playlistSettings = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[2]/div[2]/div[2]/div/div/button')
    playlistSettings.click()
    time.sleep(1)
    editDetails = driver.find_element(By.XPATH, '//*[@id="context-menu"]/ul/li[2]/button')
    editDetails.click()
    nameField = driver.find_element(By.XPATH, '//input[@data-testid="playlist-edit-details-name-input"]')
    nameField.clear()
    nameField.send_keys(name)
    descriptionField = driver.find_element(By.XPATH, '//textarea[@data-testid="playlist-edit-details-description-input"]')
    descriptionField.send_keys("Playlist generat automat cu Selenium si Python")

    save = driver.find_element(By.XPATH, '/html/body/div[22]/div/div/div/div[2]/div[4]/button')
    save.click()
    time.sleep(2)

    #inscriere cantece:
    searchbar = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/section/div/div/input')
    for row in df.itertuples():
        searchbar.send_keys(row.Nume_Cantec +" "+ row.Artist)
        time.sleep(2)
        try:
            firstItem = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div/div[1]/div/div[2]/div[1]/div/div[4]/button')
            firstItem.click()
        except:
            print("Soung couldn't be found")
        try:
            clear = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/section/div/div/div/button')
            clear.click()
        except:
            print("Eroare in program")
            exit(1)

        time.sleep(2)
    print("Playlist Created: ")
    return driver.current_url

    #song searching