import pandas as pd
from scraper import *




if __name__ == "__main__":

    driver = setDriver()
    #Get title
    searchText ="car drive vintage"
    playlistsFound = ['2lXdqHGwllSHFwXnngwBG4', '2xPSpt8gTScUxEgWF2GbUO']
    #playlistsFound = ['']

    #inainte sa schimb 10le static de aici sa fac implementarea pe care am comentat-o in functie in scraper.py
    #playlistsFound.append(searchSpotify(driver, searchText, 10))

    #trec prin fiecare playlist 
    songs=[]

    columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Plays']
    df = pd.DataFrame(songs, columns=columns)
    df = collectSongs(driver, df, playlistsFound)
    print(df)
    df.to_csv('output.csv', index=False) 

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