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

def setUpCityLatDatabase(city, lat_and_long, cur, conn):
    city_list = []
    lat_li = []
    long_li = []

    cur.execute("DROP TABLE IF EXISTS Locations")
    cur.execute("CREATE TABLE Locations (Rest_address TEXT, Latitude REAL, Longitude REAL)") #make address primary key

    for i in city:
        city_list.append(i)
    for i in lat_and_long:
        lat_li.append(i)
        long_li.append(i)

    for i in range(len(city_list)):
        cur.execute("INSERT INTO Locations (Rest_address, Latitude, Longitude) VALUES (?,?,?)",(city_list[i], lat_li[i], long_li[i]))
    conn.commit()
#sets up a database

def main():
    cur, conn = setUpDatabase('Lat&Long.db')
    city_list = ['Detroit', 'Atlanta']
    
    for i in city_list:
        get_Google_data(i)
        setUpCityLatDatabase(city_list, i, cur, conn)


if __name__ == "__main__":
    main()



