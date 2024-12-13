# Proiect-Web-Scraping

## Spotify Playlist Creator using Web automation w/ Selenium, API calls, Python

Algoritmul de rulare:
- programul primeste input titlul dorit pentru playlistul final
- pe baza lui, cauta playlisturile deja existente si le inregistreaza ID-urile
- fiecare playlist, si piesa din playlist este parcursa, iar informatiile sunt stocate intr-un dataframe Pandas
- datele sunt prelucrate in dataframe astfel incat sa fie alese cele mai unice piese
- este construit un nou playlist
- este returnat linkul catreplaylist-ul generat

### Programul ofera optiunea de a rula algoritmul prin Selenium (mai incet) sau prin Spotify API (mai rapid)