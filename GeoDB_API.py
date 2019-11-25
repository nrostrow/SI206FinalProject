import requests
import json

# empty for now, you can test by adding 'Q60' (new york city)
city_codes = []
# full city_codes list
# city_codes = ['Q60', 'Q65', 'Q1297', 'Q16555', 'Q1345', 'Q16556', 'Q975', 'Q16552', 'Q16557', 'Q16553', 'Q16559', 'Q16568', 'Q62', 'Q6346', 'Q16567', 'Q16558', 'Q16565', 'Q5083', 'Q16554', 'Q16562', 'Q12439', 'Q61', 'Q100', 'Q16563', 'Q23197']
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
