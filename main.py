import pandas as pd
from scraper import *




if __name__ == "__main__":

    driver = setDriver()
    #Get title
    searchText ="car drive vintage"
    playlistsFound = []

    #inainte sa schimb 10le static de aici sa fac implementarea pe care am comentat-o in functie in scraper.py
    playlistsFound.append(searchSpotify(driver, searchText, 10))

    print(playlistsFound)
"""
    principal()

    print("Link to playlist: ")
    link = input()
    driver.get(link)

    resetCSV()

    table = setTable(driver)
    getTracks(table)

    writeTxtFile(driver, link)

    driver.quit()
    exit(1)
"""