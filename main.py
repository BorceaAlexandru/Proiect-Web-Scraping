import pandas as pd
from scraper import *




if __name__ == "__main__":

    driver = setDriver()
    #Get title
    searchText ="car drive vintage"
    playlistsFound = []
    #playlistsFound.append(searchSpotify(driver, searchText))
    searchSpotify(driver, searchText)
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