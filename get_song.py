import requests, json, os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(THIS_DIR, 'credentials.json')
with open(creds_path, "r") as f:
    creds = json.load(f)
access_token = creds['ACCESS_TOKEN']
songs_url = 'https://api.genius.com/songs/{id}'
song_id = 378195
song_get = requests.get(songs_url.format(id=song_id), headers={'Authorization': 'Bearer ' + access_token})
data = song_get.json()
with open('song.json', 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)