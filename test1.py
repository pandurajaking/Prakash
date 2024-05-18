import requests as s

url = 'https://cpvod.testbook.com/659ba2ba1ffd3734c48d6498/playlist.m3u8'

resp = s.get('https://app.magmail.eu.org/get_keys', json={'link': url})

if resp.status_code == 200:
    headers = {
        'Host': 'app.magmail.eu.org',
        'user-agent': 'Mobile-Android',
        'device-id': 'c28d3cb16bbdac01',
        'device-details': 'Xiaomi_Redmi 7_SDK-32',
        'accept-encoding': 'gzip, deflate, br',
    }

    params = {'link': url}

    response = s.get('https://app.magmail.eu.org/get_keys', headers=headers, params=params)
    
    if response.status_code == 200:
        url1 = response.json()['url']
    else:
        url1 = url
        
    print(resp.text)
else:
    print("Failed to get response:", resp.status_code)
