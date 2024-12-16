# Proiect-Web-Scraping

## Spotify Playlist Creator using Web automation w/ Selenium, API calls, Python

Algoritmul de rulare:
- Programul primeste input titlul dorit pentru playlistul final
- Pe baza lui, cauta playlisturile deja existente si le inregistreaza ID-urile
- Fiecare playlist, si piesa din playlist este parcursa, iar informatiile sunt stocate intr-un dataframe Pandas
- Datele sunt prelucrate in dataframe astfel incat sa fie alese cele mai unice piese
- Este construit un nou playlist
- Este returnat linkul catre playlist-ul generat

### Programul ofera optiunea de a rula algoritmul prin Selenium (mai incet) sau prin Spotify API (mai rapid)
Pentru publicarea programului a fost creat un fisier .gitignore pentru a ascunde fisierele cu informatii sensibile precum API keys, username si parola