import pandas as pd
from scraper import *
from logSpotify import *




if __name__ == "__main__":

    driver = setDriver()
    #Get title
    searchText ="car drive vintage"
    #playlistsFound = ['2lXdqHGwllSHFwXnngwBG4', '2xPSpt8gTScUxEgWF2GbUO']

    #inainte sa schimb 10le static de aici sa fac implementarea pe care am comentat-o in functie in scraper.py
    playlistsFound = searchSpotify(driver, searchText, 10)
    print(playlistsFound)

    #trec prin fiecare playlist 
    songs=[]

    columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Plays']
    df = pd.DataFrame(songs, columns=columns)
    df = collectSongs(driver, df, playlistsFound)
    print(df)
    df.to_csv('output.csv', index=False)
    driver.close()

    #de prelucrat coloana cu scor dupa care sa maiau

    df = pd.read_csv('output.csv')
    df = df.sort_values('NumarAparitii', ascending=False).head(30)
    print(df)
    finalLink = playlistCreation(df,searchText)
    print(finalLink)

