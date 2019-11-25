import requests
import json

city_codes = ['Q60']
base_url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/"
headers = {
    'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
    'x-rapidapi-key': "e9557b3be3msh2ca132a52dbbc5bp1e9aacjsna6acb3f99a0d"
}

for code in city_codes:
    url = base_url + code
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    info = (data['data']['name'], data['data']['elevationMeters'], data['data']['population'], data['data']['timezone'])
    print(info)
