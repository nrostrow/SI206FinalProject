import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import os

def connect_db(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def plot_population_elevation(cur, conn):
    elevations = []
    populations = []
    cur.execute("SELECT elevation, population FROM CityInfo INNER JOIN CityPop ON CityInfo.city_name = CityPop.city_name")
    rows = cur.fetchall()
    for row in rows:
        elevations.append(row[0])
        populations.append(row[1])
    plt.scatter(elevations, populations)
    plt.xlabel('Elevation (M)')
    plt.ylabel('Population')
    plt.title('City Elevation vs Population')
    plt.grid()
    plt.autoscale()
    plt.savefig("population_elevation.png", bbox_inches='tight')

def get_city_reviews(cur, conn):
    cities = []
    reviews = []
    store = {}
    cur.execute("SELECT city_name FROM CityInfo")
    rows = cur.fetchall()
    for row in rows:
        cities.append(row[0])
    cur.execute("SELECT city, reviews FROM Yelp")
    rows = cur.fetchall()
    for row in rows:
        store[row[0]] = store.get(row[0], 0) + int(row[1])
    for city in cities:
        reviews.append(store.get(city, 0))
    print(cities)
    print(reviews)

def main():
    cur, conn = connect_db('data.db')
    #plot_population_elevation(cur, conn)
    get_city_reviews(cur, conn)

if __name__ == "__main__":
    main()