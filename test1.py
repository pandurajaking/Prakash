import requests as s

session = s.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
})

resp = session.post(
    'https://app.magmail.eu.org/get_keys',
    json={'link': 'https://cpvod.testbook.com/659ba2ba1ffd3734c48d6498/playlist.m3u8'}
)

print(resp.text)
