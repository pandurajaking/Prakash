import requests as s

resp = s.post('https://app.magmail.eu.org/get_keys', json={'link':'https://cpvod.testbook.com/659ba2ba1ffd3734c48d6498/playlist.m3u8'})

print(resp.text)