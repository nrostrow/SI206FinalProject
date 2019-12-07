import requests
import json
import unittest
import sqlite3
import os

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
    params={'term':'restaurant', 'location': 'Detroit' } #'sort_by': "review_count" 
    req = requests.get(url, params=params, headers=headers)
    #print('the status code is {}'.format(req.status_code))
    parsed = json.loads(req.text)
    print(json.dumps(parsed, indent=4))
    businesses = parsed["businesses"]
    # for business in businesses:
    #     print("Name:", business["name"])
    #     print("City:", business["location"]["city"])
    #     print("Rating:", business["rating"])
    #     print("Address:", " ".join(business["location"]["display_address"]))
    #     print("Phone:", business["phone"])
    #     print("Total Reviews:" ,business["review_count"])
    #     #print("Price Range:", business["price"])
    #     print("Category:", business["categories"][0]["title"])
    #     print("\n")
    return parsed

def Database_builder(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn
    

# def setUpCateogriesTable(data, cur, conn):
#     category_list = []
#     for business in data['businesses']:
#         business_categories = business['categories']
#         for category in business_categories:
#             if category['title'] not in category_list:
#                 category_list.append(category['title'])

#     cur.execute("DROP TABLE IF EXISTS Categories")
#     cur.execute("CREATE TABLE Categories (city TEXT PRIMARY KEY, title TEXT)")
#     for i in range(len(category_list)):
#         cur.execute("INSERT INTO Categories (city,title) VALUES (?,?)",(i,category_list[i]))
#     conn.commit()
def City_list_creator():

    pass
def Yelp_data_populate(data, cur, conn):
    id_list = []
    name_list = []
    city_list = []
    address_list = []
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

        zipcode = i['location']
        zipcode_list.append(zipcode["zip_code"])
        

        phone_num = i['phone']
        phone_list.append(phone_num)

        rating = i['rating']
        rating_list.append(rating)

        reviews = i['review_count']
        reviewcount_list.append(reviews)

    for i in range(len(city_list)):
        cur.execute("INSERT INTO Yelp (restaurant_id ,name, city, phone_num, rating, reviews) VALUES (?,?,?,?,?,?)",(id_list[i],name_list[i],city_list[i],phone_list[i],rating_list[i],reviewcount_list[i]))
        cur.execute("INSERT INTO YelpAddress (restaurant_id, address, city, zipcode) VALUES (?,?,?,?)",(id_list[i],address_list[i],city_list[i],zipcode_list[i]))
    conn.commit()
def Yelp_data_setup(data, cur, conn):
    # id_list = []
    # name_list = []
    # city_list = []
    # address_list = []
    # phone_list = []
    # rating_list = []
    # reviewcount_list = []

    # for i in data["businesses"]:
    #     ID = i['id']
    #     id_list.append(ID)

    #     name = i['name']
    #     name_list.append(name)

    #     city = i['location']['city']
    #     city_list.append(city)

    #     address =  i['location']
    #     address_list.append(address['address1'])

    #     phone_num = i['phone']
    #     phone_list.append(phone_num)

    #     rating = i['rating']
    #     rating_list.append(rating)

    #     reviews = i['review_count']
    #     reviewcount_list.append(reviews)

    cur.execute("DROP TABLE IF EXISTS Yelp")
    cur.execute("DROP TABLE IF EXISTS YelpAddress")
    
    cur.execute("CREATE TABLE Yelp (restaurant_id TEXT PRIMARY KEY,name TEXT, city TEXT, phone_num TEXT, rating REAL, reviews INTEGER)")
    cur.execute("CREATE TABLE YelpAddress(restaurant_id TEXT PRIMARY KEY, address TEXT, city TEXT, zipcode TEXT)")
    conn.commit()
    # for i in range(len(city_list)):
    #     cur.execute("INSERT INTO Yelp (restaurant_id ,name, city, address, phone_num, rating, reviews) VALUES (?,?,?,?,?,?,?)",(id_list[i],city_list[i],name_list[i],address_list[i],phone_list[i],rating_list[i],reviewcount_list[i]))
    # conn.commit()
def create_database(data, cur, conn):
    Yelp_data_setup(location(api_key), cur, conn)

cur, conn = Database_builder('yelp.db')
#setUpCateogriesTable(location(api_key), cur, conn)
#Yelp_data_setup(location(api_key), cur, conn)
create_database(location(api_key), cur, conn)
Yelp_data_populate(location(api_key), cur, conn)
#location(api_key)