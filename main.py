import pandas as pd
from scraper import *
from logSpotify import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

def APIwork(df, playlistsFound):
    client_id = "3464824c61514e52b2b21a4082386cf9"
    client_secret = "ac70f9a0650443e3ba5b334086a33f98"
    # Authenticate
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Fetch playlist details
    for playlistID in playlistsFound:
        ok = 1
        print("Incep un playlist")
        try:
            playlist = sp.playlist(playlistID)
        except:
            print("Playlist Invalid")
            ok = 0
        if(ok):
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

    print("Alege un titlu general pentru playlist: ")
    searchText = input()
    playlistsFound = searchSpotify(driver, searchText, 10)

    print("Metoda rapida sau inceata (r/i): ")
    response = input()

    if(response == "i"):
        songs=[]

        columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Plays']
        df = pd.DataFrame(songs, columns=columns)
        df = collectSongs(driver, df, playlistsFound)
        print(df)
        df.to_csv('output.csv', index=False)
        driver.close()

        df = pd.read_csv('output.csv')
        df = df.sort_values('NumarAparitii', ascending=False).head(30)
    elif(response == "r"):
        driver.close()
        songs=[]
        columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Plays']
        df = pd.DataFrame(songs, columns=columns)
        APIwork(df, playlistsFound)
        df = df[df['Plays'] >= 10]
        df.to_csv('output2.csv', index=False)
        df['Score'] = df['NumarAparitii'] / df['Plays']
        # df = df.sort_values('Plays', ascending=False).head(30)
        df = df.sort_values('Score', ascending=False).head(30)
        print(df)
    else:
        print("Optiune invalida. Programul se va opri!")
        exit(1)

    finalLink = playlistCreation(df,searchText)
    print(finalLink)
