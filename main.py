import pandas as pd
from scraper import *
from logSpotify import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

def APIwork(df, playlistsFound):
    client_id = "8d6985f70c314009838c213744be7a33"
    client_secret = "d07c6c7043824f3685f0678c839057ec"
    # Authenticate
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Fetch playlist details
    for playlistID in playlistsFound:
        print("Incep un playlist")
        playlist = sp.playlist(playlistID)
        for song in playlist["tracks"]["items"]:
            try:
                aux =[]
                ID = song["track"]["id"]
                songDetails = sp.track(ID)
                if (songDetails["is_local"]): break
                artistName = songDetails["artists"]
                allArtists =''
                for artists in artistName:
                    allArtists += artists["name"] +", "

                aux.append(ID)
                aux.append(songDetails["name"])
                aux.append(allArtists[:-2])#artist
                aux.append(1)
                aux.append(1)# nu mege is playable
                aux.append(songDetails["popularity"])
                addToDf(aux, df)
            except:
                print("Skipped track")



if __name__ == "__main__":

    driver = setDriver()
    #Get title
    searchText ="car drive vintage"
    #playlistsFound = ['2lXdqHGwllSHFwXnngwBG4', '2xPSpt8gTScUxEgWF2GbUO']

    #inainte sa schimb 10le static de aici sa fac implementarea pe care am comentat-o in functie in scraper.py
    playlistsFound = searchSpotify(driver, searchText, 10)
    print(playlistsFound)
    """
    #trec prin fiecare playlist 
    songs=[]

    columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Plays']
    df = pd.DataFrame(songs, columns=columns)
    df = collectSongs(driver, df, playlistsFound)
    print(df)
    df.to_csv('output.csv', index=False)
    driver.close()
    """
    driver.close()
    songs=[]
    columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Plays']
    df = pd.DataFrame(songs, columns=columns)
    APIwork(df, playlistsFound)
    #df['Score'] = df['NumarAparitii'] / df['Plays']
    df = df.sort_values('Plays', ascending=False).head(30)
    print(df)

    #de prelucrat coloana cu scor dupa care sa maiau
    """
    df = pd.read_csv('output.csv')
    df = df.sort_values('NumarAparitii', ascending=False).head(30)
    print(df)
    finalLink = playlistCreation(df,searchText)
    print(finalLink)
    """

