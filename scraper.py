from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import html

def setDriver():

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver

def searchSpotify(driver, searchText, playlistCounter):
    driver.get("https://open.spotify.com/")
    #time.sleep(1)
    searchBar = driver.find_element(By.XPATH, '//*[@id="global-nav-bar"]/div[2]/div/div/span/div/form/div[2]/input')
    searchBar.send_keys(searchText)
    searchBar.send_keys(Keys.ENTER)

    playlistButton = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/div[1]/div/div/div[1]/div/a[4]/button')
    playlistButton.click()
    

    table = driver.find_element(By.XPATH, '//*[@id="searchPage"]/div/div/div/div[1]')
    playlistIDs = []
    counter = 1     #will have to find the 1st
    while(1):
        playlist = table.find_element(
            By.XPATH, "./span["+str(counter)+"]/div/div/div[2]"
        )

        playlistID = playlist.get_attribute("id")[28 : -2]
        currentPlaylist =playlist.get_attribute("id").split("-")[-1]

        driver.execute_script("arguments[0].scrollIntoView();", playlist)

        if(counter != int(currentPlaylist)+1):  
            print("Greseala undeva")
            exit(1)

        playlistIDs.append(playlistID)
        counter = counter + 1

        if(counter >= playlistCounter):
            print("Gata colectarea")
            break;   
    
    #este nevoie de o implementare pentru atunci cand trec de numarul de span-uri
    #puse static in html si va trebui sa le incarc dinamic si sa iau numaratoarea de la counterul pe care il am deja
    #momentan, lucrez cu 10, daca voi mai avea timp mai fac
    time.sleep(10)
    return playlistIDs

def addToDf(track_info, df):
    #aici pun conditii sa nu se dubleze
    if track_info[0] in df['ID'].values:
        df.loc[df['ID'] == track_info[0], 'NumarAparitii'] += 1
    else:
        df.loc[len(df)] = track_info

def getPlays(driver2, trackID):
    driver2.get(trackID)
    number = 0
    try:
        plays = driver2.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/div/span[8]')
        number = int(plays.get_attribute('innerHTML').replace(',', ''))
    except:
        print("Plays not found :/")
    return number

def getTracks(driver, table, df, driver2):
    index = 2
    #tot ce am mai jos in while 1
    while(1):
        try:
            track = table.find_element(
                By.XPATH, "./div[@aria-rowindex='" + str(index) + "']"
            )
        except:
            print("\nAll songs have been scanned")
            break
        driver.execute_script("arguments[0].scrollIntoView();", track)

        track_info = []         #columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Plays']

        #trackID
        trackID =track.find_element(By.XPATH, './div/div[2]/div/a').get_attribute("href")
        track_info.append(trackID)

        try:
            track_data = track.find_element(
                By.CSS_SELECTOR, 'div > div[aria-colindex="2"] > div '
            )
            track_name = track_data.find_element(
                By.CSS_SELECTOR, "a > div"
            ).get_attribute("innerHTML")
            track_artist = track_data.find_elements(
                By.CSS_SELECTOR, "span.standalone-ellipsis-one-line > div > a"
            )
            track_avalability = 1
        except:
            track_name = "Unavalable song"
            track_artist = []
            track_avalability = 0

        #track name
        track_info.append(html.unescape(track_name))

        output_artists = ""
        for artist in track_artist:
            output_artists += artist.get_attribute("innerHTML") + ", "
        
        if(len(output_artists)): output_artists = output_artists[:-2]

        #track artists
        track_info.append(html.unescape(str(output_artists)))
        #track numar de aparitii
        track_info.append(1)
        #track avalability
        track_info.append(track_avalability)
        #track_plays
        if(track_avalability):
            track_info.append(getPlays(driver2, trackID))
        else:
            track_info.append(100000000000)
        #track_info.append(0)

        addToDf(track_info, df)

        index = index + 1

def scrapePlaylist(driver, playlistName, df, driver2):
    #iau fiecare cantec in parte
    driver.get("https://open.spotify.com/playlist/" + playlistName)
    table = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]',
    )
    #//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]
    getTracks(driver, table, df, driver2)

def collectSongs(driver, df, playlistsFound):
    driver2 = setDriver()
    #iau fiecare playlist in parte
    for playlistInstance in playlistsFound:
        print(playlistInstance)
        scrapePlaylist(driver, playlistInstance, df, driver2)
    
    driver2.close()

    return df

