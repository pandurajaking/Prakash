import requests as s

url = 'https://cpvod.testbook.com/659ba2ba1ffd3734c48d6498/playlist.m3u8'

resp = s.get('https://app.magmail.eu.org/get_keys', json={'link': url})
print(resp.text)
