import requests 
import json
import re
import sqlite3
import os


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
#Returns Latitude and Longitude


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
# Function to set up the main database, called final.db

def setUpCityLatDatabase(address, lat_and_long, cur, conn):
    lat = lat_and_long[0]
    #lat_li.append(lat)
    #appends first element of the list lat_and_long
    lon = lat_and_long[1]
    #long_li.append(lon)
    #appends second element of the list lat_and_long
        
    cur.execute("INSERT INTO Latitude (Address, Latitude) VALUES (?,?)",(address, lat))
        #Inserts data into the Latitude table
    cur.execute("INSERT INTO Longitude (Address, Longitude) VALUES (?,?)",(address, lon))
    conn.commit()
#sets up a database

def main():
    cur, conn = setUpDatabase('Lat&Long.db')

    cur.execute("CREATE TABLE IF NOT EXISTS Latitude (Address TEXT PRIMARY KEY, Latitude REAL)") 
    #Creates first table for API, with the address and latitude

    cur.execute("CREATE TABLE IF NOT EXISTS Longitude (Address TEXT PRIMARY KEY, Longitude REAL)") 
    #Creates second table for API, with the address and longitude

    address_list = ['12025 Brandywine Drive Brighton, MI', '800 Fuller St AnnArbor, MI']
    
    for i in address_list:
        lat_and_long = get_Google_data(i)

        setUpCityLatDatabase(i, lat_and_long, cur, conn)


if __name__ == "__main__":
    main()



