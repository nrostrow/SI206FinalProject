import requests
import json


api_key='LS5XDJMhLBven3IcI5NFLb8Izy51zMVtz00PY7RpDtlUeOvoPr0jLmVIriDNjWcWft146AaheyIzozbdRgMSRwMS8edXYcjZQHob1dhg_FKyAbeRukYTOs3YSUHcXXYx'
headers = {'Authorization': 'Bearer %s' % api_key}
def Reviews(api_key):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = "https://api.yelp.com/v3/businesses/FEVQpbOPOwAPNIgO7D3xxw/reviews"
    req = requests.get(url, headers=headers)
    print('the status code is {}'.format(req.status_code))
    print(json.loads(req.text))

def location(api_key):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/search'
    params={'term':'restaurant', 'location': "Detroit" } #'sort_by': "review_count" 
    req = requests.get(url, params=params, headers=headers)
    #print('the status code is {}'.format(req.status_code))
    parsed = json.loads(req.text)
    #print(json.dumps(parsed, indent=4))
    businesses = parsed["businesses"]
    for business in businesses:
        print("Name:", business["name"])
        print("City:", business["location"]["city"])
        print("Rating:", business["rating"])
        print("Address:", " ".join(business["location"]["display_address"]))
        print("Phone:", business["phone"])
        print("Total Reviews:" ,business["review_count"])
        #print("Price Range:", business["price"])
        print("Category:", business["categories"][0]["title"])
        print("\n")

location(api_key)