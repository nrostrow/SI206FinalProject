import requests 
import json
import re


def get_Google_data(data):

    lat_long_list = []
    api_key = 'AIzaSyAg9jsCeHF3VjdMJqEAuT90fpArAXQZld4'
    #API key given from Google
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={},{},{}&key={}'
    #From Documentation

    data = re.sub(r'[^\w\s]','',data)
    #To get rid of the comma, and to forget the zip code
    data_pieces = data.split()
    street1 = data_pieces[0:-3]
    s = " "
    street = s.join(street1) 
    city = data_pieces[-3]
    state = data_pieces[-2]
    #Need to split up data, into pieces of address in order to put them in url

    request_url = base_url.format(street, city, state, api_key)
    #Need to pass in these parameters in order to have a complete request
    r = requests.get(request_url)
    data = r.text
    data_dict = json.loads(data)
    
    #print(json.dumps(data_dict,indent=4))
    results = data_dict["results"]
    for result in results:
        lat = result["geometry"]['location']["lat"]
        lat_long_list.append(lat)
        lon = result["geometry"]['location']['lng']
        lat_long_list.append(lon)

    return lat_long_list

def main():
    data = "644 Selden hi St Detroit, MI 48201"
    get_Google_data(data)

if __name__ == "__main__":
    main()



