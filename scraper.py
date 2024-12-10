from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
#import csv
#import xlwt
#from xlwt import Workbook

#MODIFICARI CLOUDSCRAPER
#import cloudscraper

def setDriver():

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver

def searchSpotify(driver, searchText, playlistCounter):
    driver.get("https://open.spotify.com/")
    time.sleep(1)
    searchBar = driver.find_element(By.XPATH, '//*[@id="global-nav-bar"]/div[2]/div/div/span/div/form/div[2]/input')
    searchBar.send_keys(searchText)
    searchBar.send_keys(Keys.ENTER)

    playlistButton = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/div[1]/div/div/div[1]/div/a[4]/button')
    playlistButton.click()
    

    table = driver.find_element(By.XPATH, '//*[@id="searchPage"]/div/div/div/div[1]')
    playlistIDs = []
    counter = 1     #will have to find the 1st
    while(1):
        print(counter)
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
        df.loc[df['ID'] == track_info['ID'], 'NumarAparitii'] += 1
    else:
        df.loc[len(df)] = track_info


def getTracks(driver, table, df):
    index = 2
    #tot ce am mai jos in while 1
    try:
        track = table.find_element(
            By.XPATH, "./div[@aria-rowindex='" + str(index) + "']"
        )
    except:
        print("\nAll songs have been scanned")
        #break
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
    track_info.append(track_name)

    output_artists = ""
    for artist in track_artist:
        output_artists += artist.get_attribute("innerHTML") + ", "
        
    if(len(output_artists)): output_artists = output_artists[:-2]

    #track artists
    track_info.append(str(output_artists))
    #track numar de aparitii
    track_info.append(1)
    #track avalability
    track_info.append(track_avalability)
    #track_plays
    track_info.append("working")


    index = index + 1

    ##add to df
    addToDf(track_info, df)
    print(track_info)


def scrapePlaylist(driver, playlistName, df):
    #iau fiecare cantec in parte
    driver.get("https://open.spotify.com/playlist/" + playlistName)
    table = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]',
    )
    #//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]
    getTracks(driver, table, df)
    time.sleep(10)

    print("im cooked2")

def collectSongs(driver, df, playlistsFound):

    #iau fiecare playlist in parte
    for playlistInstance in playlistsFound:
        scrapePlaylist(driver, playlistInstance, df)
    
    print("Im cooked")

    return df























"""

FUNCTIA INITIALA "PRELUCRARE DATE"

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


def prelucrareDate(driver, game):
    #print(f"Procesare joc: {game}")
    data_list=[game]

    #scraper
    #scraper=cloudscraper.create_scraper(browser='chrome')
    scraper = cloudscraper.create_scraper()
    print(scraper.get("https://steamdb.info/app/{game}/charts/").text)
    time.sleep(10)
    #url=f"https://steamdb.info/app/{game}/charts/"


    response = scraper.get(url)

    if response.status_code != 200:
        print(f"Eroare la pag jocului {game}")
        return data_list

    #cica asta incarca sursa pag in selenium ??
    driver.execute_script("document.body.innerHTML = arguments[0];", response.text)
    #try catch
    try:

        response=scraper.get(url)
        print(f"Cod status pentru {game}: {response.status_code}")

        if response.status_code != 200:
            raise Exception("Pagina nu poate fi accesata!")

        #driver.execute_script("document.body.innerHTML = arguments[0];", response.text)

        game_name = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/div[1]/h1').get_attribute("innerHTML")
        steam_db_rating = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[2]/strong').get_attribute("innerHTML")[:-1]
        positive_reviews = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[3]/strong').get_attribute("innerHTML")
        negative_reviews = driver.find_element(By.XPATH, '//*[@id="charts"]/ul[2]/li[4]/strong').get_attribute("innerHTML")
        followers = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[1]/ul/li[1]/strong').get_attribute("innerHTML")
        peak24 = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[2]/ul/li[1]/strong').get_attribute("innerHTML")
        peak_all_time = driver.find_element(By.XPATH, '//*[@id="charts"]/div[4]/div[2]/ul/li[3]/strong').get_attribute("innerHTML")

        data_list.append([game_name, steam_db_rating, positive_reviews, negative_reviews, followers, peak24, peak_all_time])

    except Exception as e:
        print(f"Eroare la pag jocului {game}:{e}")

    return data_list
    

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
    #wb=xlwt.Workbook()
    #sheet1 = wb.add_sheet("Sheet1", cell_overwrite_ok=False)

    list_final = []
    f=open("games.csv", "w")
    writer=csv.writer(f)
    #i=0
    for game in gamesID:

        list_final.append(prelucrareDate(driver, game))
        #writer.writerows(prelucrareDate(driver, game))

        list_final.append(prelucrareDate(driver, game))
        sheet1.write(i+1, 1, list_final[i])
        i=i+1


    print(list_final)
    #wb.save("xlwt GameData.xlsx")
    f.close()


"""