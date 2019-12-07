import requests
import json
import sqlite3
import os

api_key='LS5XDJMhLBven3IcI5NFLb8Izy51zMVtz00PY7RpDtlUeOvoPr0jLmVIriDNjWcWft146AaheyIzozbdRgMSRwMS8edXYcjZQHob1dhg_FKyAbeRukYTOs3YSUHcXXYx'
headers = {'Authorization': 'Bearer %s' % api_key}

# We probably don't need this
def Reviews(api_key):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = "https://api.yelp.com/v3/businesses/FEVQpbOPOwAPNIgO7D3xxw/reviews"
    req = requests.get(url, headers=headers)
    print('the status code is {}'.format(req.status_code))
    print(json.loads(req.text))

def location(api_key, city):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/search'
    params={'term':'restaurant', 'location': city }
    req = requests.get(url, params=params, headers=headers)
    parsed = json.loads(req.text)
    return parsed

def Database_builder(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn
    
def City_list_creator(cur, conn):
    cities = []
    cur.execute("SELECT city_name FROM CityPop")
    rows = cur.fetchall()
    for row in rows:
        cities.append(row[0])
    return cities

def Yelp_data_populate(data, cur, conn):
    id_list = []
    name_list = []
    city_list = []
    address_list = []
    state_list = []
    zipcode_list = []
    phone_list = []
    rating_list = []
    reviewcount_list = []

    for i in data["businesses"]:
        ID = i['id']
        id_list.append(ID)

        name = i['name']
        name_list.append(name)

        city = i['location']['city']
        city_list.append(city)

        address =  i['location']
        address_list.append(address['address1'])

        state = i['location']['state']
        state_list.append(state)

        zipcode = i['location']
        zipcode_list.append(zipcode["zip_code"])
        
        phone_num = i['phone']
        phone_list.append(phone_num)

        rating = i['rating']
        rating_list.append(rating)

        reviews = i['review_count']
        reviewcount_list.append(reviews)

    for i in range(len(city_list)):
        try:
            cur.execute("INSERT INTO Yelp (restaurant_id ,name, city, phone_num, rating, reviews) VALUES (?,?,?,?,?,?)",(id_list[i],name_list[i],city_list[i], phone_list[i],rating_list[i],reviewcount_list[i]))
            cur.execute("INSERT INTO YelpAddress (restaurant_id, address, city, zipcode, state) VALUES (?,?,?,?,?)",(id_list[i],address_list[i],city_list[i],zipcode_list[i], state_list[i]))
        except:
            print(name_list[i], city_list[i])
    conn.commit()

def Yelp_data_setup(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Yelp")
    cur.execute("DROP TABLE IF EXISTS YelpAddress")
    
    cur.execute("CREATE TABLE Yelp (restaurant_id TEXT PRIMARY KEY,name TEXT, city TEXT, phone_num TEXT, rating REAL, reviews INTEGER)")
    cur.execute("CREATE TABLE YelpAddress(restaurant_id TEXT PRIMARY KEY, address TEXT, city TEXT, zipcode TEXT, state TEXT)")
    conn.commit()

def create_database(cur, conn):
    Yelp_data_setup(cur, conn)


cur_yelp, conn_yelp = Database_builder('yelp.db')
cur_cities, conn_cities = Database_builder('cities.db')
cities = City_list_creator(cur_cities, conn_cities)
#create_database(cur_yelp, conn_yelp)
for city in cities:
    Yelp_data_populate(location(api_key, city), cur_yelp, conn_yelp)
#Yelp_data_populate(location(api_key), cur_yelp, conn_yelp)
