import json, os, requests
from bs4 import BeautifulSoup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(THIS_DIR, 'credentials.json')
with open(creds_path, 'r') as f:
    creds = json.load(f)
access_token = creds['ACCESS_TOKEN']

artist_id = 16775
songs_url = 'https://api.genius.com/artists/{id}/songs'.format(id=artist_id)
headers = {'Authorization': 'Bearer ' + access_token}
songs_get = requests.get(songs_url, headers=headers)
data = songs_get.json()
lyric_d = dict()
while 1:
    for song in data['response']['songs']:
        song_url = song['url']
        song_get = requests.get(song_url)
        song_text = song_get.text
        html1 = BeautifulSoup(song_text, 'html.parser')
        html2 = str(html1.find('div', {'data-lyrics-container': True})).replace('<br/>', '\n')
        lyrics = BeautifulSoup(html2, 'html.parser').text
        lyric_d[song['title']] = lyrics
    next_page = data['response']['next_page']
    if next_page == None:
        break
    next_page_url = songs_url + '?page=' + str(next_page)
    songs_get = requests.get(next_page_url, headers=headers)
    data = songs_get.json()
with open('lyrics.json', 'w') as f:
    json.dump(lyric_d, f, indent=4, ensure_ascii=False)