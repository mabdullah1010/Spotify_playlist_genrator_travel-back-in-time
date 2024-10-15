import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import openvpn_api
from spotipy.oauth2 import SpotifyClientCredentials

user_reply = input("Which date do you want to travel to? Type date in this format YYYY-MM-DD : ")
URL = "https://www.billboard.com/charts/hot-100/" + user_reply

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

song_titles = []

chart_list = soup.find_all('li', class_='o-chart-results-list__item')

for i in range(140):
    title_tag = chart_list[i].find('h3', class_='c-title')
    if title_tag:
        song_titles.append(title_tag.get_text(strip=True))

song_urls = []
for song in song_titles:
    try:
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(

            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"]))
        song_details = spotify.search(q=song, limit=1, offset=0, type="track")
        print(f"{song}: {song_details["tracks"]["items"][0]["external_urls"]["spotify"]}")
        song_urls.append(song_details["tracks"]["items"][0]["external_urls"]["spotify"])
    except:
        print(f"{song} not found on spotify")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["CLIENT_ID"],
                                               client_secret=os.environ["CLIENT_SECRET"],
                                               redirect_uri='https://developer.spotify.com/dashboard',
                                               scope='playlist-modify-public'))

# Now call the instance method on the Spotify object
new_playlist = sp.user_playlist_create(user=os.environ[USER_ID],
                                       name=f"{user_reply} - hot 10 songs",
                                       public=True,
                                       collaborative=True,
                                       description="abc")

playlist_url = new_playlist["external_urls"]["spotify"]
playlist_id = new_playlist["id"]
print(f" Your Playlist's URL is : {playlist_url}")

add_song = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri='https://developer.spotify.com/dashboard',
))
added = add_song.playlist_add_items(playlist_id=playlist_id, items=song_urls[0: 10])
print(added)
c = input("press any key to exit")
