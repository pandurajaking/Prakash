import requests

url = 'https://cpvod.testbook.com/659ba2ba1ffd3734c48d6498/playlist.m3u8'

headers = {
    'Host': 'app.magmail.eu.org',
    'User-Agent': 'Mobile-Android',
    'Device-ID': 'c28d3cb16bbdac01',
    'Device-Details': 'Xiaomi_Redmi 7_SDK-32',
    'Accept-Encoding': 'gzip, deflate, br',
}

resp = requests.post('https://app.magmail.eu.org/get_keys', json={'link': url}, headers=headers)

print(resp.text)
