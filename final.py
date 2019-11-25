import requests 
import json


def get_Google_data(street, city, state):

    api_key = 'AIzaSyAg9jsCeHF3VjdMJqEAuT90fpArAXQZld4'
    #API key given from Google
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={},{},{}&key={}'
    #From Documentation
    request_url = base_url.format(street, city, state, api_key)
    #Need to pass in these parameters in order to have a complete request
    r = requests.get(request_url)
    data = r.text
    data_dict = json.loads(data)
    
    print(json.dumps(data_dict,indent=4))
    results = data_dict["results"]
    for result in results:
        print(result["geometry"]['location']["lat"])
        print(result["geometry"]['location']['lng'])
        print(result)

#get_Google_data("644 Selden St","Detroit", "MI")
#644 Selden St Detroit, MI 48201
def wild():
    data = "644 Selden St Detroit MI"
    data_pieces = data.split()
    street1 = data_pieces[0:3]
    s = " "
    street2 = s.join(street1) 
    city1 = data_pieces[3]
    state1 = data_pieces[4]
    #print(street)
    #print(city)
    #print(state)
    get_Google_data(street2, city1, state1)

wild()
["664","selden",'street']
# if __name__ == "__main__":
#     test_it()


