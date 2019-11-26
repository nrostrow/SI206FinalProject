import requests 
import json


def get_Google_data(data):

    api_key = 'AIzaSyAg9jsCeHF3VjdMJqEAuT90fpArAXQZld4'
    #API key given from Google
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={},{},{}&key={}'
    #From Documentation


    data_pieces = data.split()
    street1 = data_pieces[0:3]
    s = " "
    street = s.join(street1) 
    city = data_pieces[3]
    state = data_pieces[4]
    #Need to split up data, into pieces of address in order to put them in url

    request_url = base_url.format(street, city, state, api_key)
    #Need to pass in these parameters in order to have a complete request
    r = requests.get(request_url)
    data = r.text
    data_dict = json.loads(data)
    
    #print(json.dumps(data_dict,indent=4))
    results = data_dict["results"]
    for result in results:
        print(result["geometry"]['location']["lat"])
        print(result["geometry"]['location']['lng'])

#get_Google_data("644 Selden St","Detroit", "MI")
#644 Selden St Detroit, MI 48201
def main():
    data = "644 Selden St Detroit MI"
  
    get_Google_data(data)

if __name__ == "__main__":
    main()



