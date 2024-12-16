import pandas as pd
from scraper import *
from logSpotify import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from credentials import id, id_secret

def APIwork(df, playlistsFound):
    client_id = id
    client_secret = id_secret
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

    print("---Aplicatie Playlist------------------------------------------")

    print("Alege un titlu general pentru playlist: ")
    searchText = input()

    print("---------------------------------------------------------------")
    print("Metoda rapida sau inceata (r/i): ")
    print("Metoda inceata demonstreaza extragerea informatiei prin webscraping iar metoda rapida prin API-ul pus la dispozitie de Spotify")
    response = input()

    print("---------------------------------------------------------------")
    driver = setDriver()
    playlistsFound = searchSpotify(driver, searchText, 10)

    songs=[]
    columns = ['ID', 'Nume_Cantec', 'Artist', 'NumarAparitii', 'Avalable', 'Popularity']
    df = pd.DataFrame(songs, columns=columns)

    if(response == "i"):
        df = collectSongs(driver, df, playlistsFound)
        print(df)

        df.to_csv('output.csv', index=False)
        print("Cantece salvate in csv")
        driver.close()

        df = pd.read_csv('output.csv')
        df = df.sort_values('NumarAparitii', ascending=False).head(30)
    elif(response == "r"):
        driver.close()
        APIwork(df, playlistsFound)

        df = df[df['Popularity'] >= 10]

        df.to_csv('output2.csv', index=False)
        print("Cantece salvate in csv")
        df['Score'] = df['NumarAparitii'] / df['Popularity']
        # df = df.sort_values('Popularity', ascending=False).head(30)
        df = df.sort_values('Score', ascending=False).head(30)
        print(df)
    else:
        print("Optiune invalida. Programul se va opri!")
        exit(1)

    finalLink = playlistCreation(df,searchText)
    print("Linkul catre playlistul final: ")
    print(finalLink)
