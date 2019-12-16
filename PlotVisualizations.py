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
    plt.scatter(elevations, populations, color='red')
    plt.xlabel('Elevation (M)')
    plt.ylabel('Population')
    plt.title('City Elevation vs Population')
    plt.grid()
    plt.autoscale()
    plt.savefig("population_elevation.png", bbox_inches='tight')

def plot_city_review(cur, conn):
    temp_cities = []
    temp_reviews = []
    cities = []
    reviews = []
    store = {}
    cur.execute("SELECT city_name FROM CityInfo")
    rows = cur.fetchall()
    for row in rows:
        temp_cities.append(row[0])
    cur.execute("SELECT city, reviews FROM Yelp")
    rows = cur.fetchall()
    for row in rows:
        store[row[0]] = store.get(row[0], 0) + int(row[1])
    for city in temp_cities:
        temp_reviews.append(store.get(city, 0))
    for i, review in enumerate(temp_reviews):
        if review > 0:
            cities.append(temp_cities[i])
            reviews.append(review)
    plt.bar(cities, reviews, color='purple')
    plt.xlabel('City')
    plt.ylabel('Review Count')
    plt.title('Total Restaraunt Review Counts Per City')
    plt.autoscale()
    plt.xticks(rotation=90)
    plt.gcf().set_size_inches(20, 5)
    plt.tight_layout()
    plt.savefig("city_reviews.png", bbox_inches='tight')

def plot_average_city_rating(cur, conn):
    temp_cities = []
    temp_ratings = []
    cities = []
    ratings = []
    store = {}
    cur.execute("SELECT city_name FROM CityInfo")
    rows = cur.fetchall()
    for row in rows:
        temp_cities.append(row[0])
    cur.execute("SELECT city, rating FROM Yelp")
    rows = cur.fetchall()
    for row in rows:
        store[row[0]] = store.get(row[0], []) + [(int(row[1]))]
    for city in temp_cities:
        city_ratings = store.get(city, [])
        if len(city_ratings) > 0:
            temp_ratings.append(sum(city_ratings) / len(city_ratings))
        else:
            temp_ratings.append(0)
    for i, rating in enumerate(temp_ratings):
        if rating > 0:
            cities.append(temp_cities[i])
            ratings.append(rating)
    plt.bar(cities, ratings, color='orange')
    plt.xlabel('City')
    plt.ylabel('Average Rating')
    plt.title('Average Restraunt Rating Per City')
    plt.autoscale()
    plt.xticks(rotation=90)
    plt.gcf().set_size_inches(20, 5)
    plt.tight_layout()
    plt.savefig("city_ratings.png", bbox_inches='tight')

    def plot_lat_long(cur, conn):
        lat = []
        lon = []
        cur.execute("SELECT Latitude, Longitude, Latitude.restaurant_id FROM Latitude INNER JOIN Longitude ON Latitude.restaurant_id = Longitude.restaurant_id")
        rows = cur.fetchall()
        for i in rows:
            lat.append(i[0])
            lon.append(i[1])
        plt.scatter(lon,lat, c = 'Black', marker = "x")
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Latitude and Longitude of Restaurants in US Cities')
        plt.savefig("lat_long.png", bbox_inches = 'tight')

def main():
    cur, conn = connect_db('data.db')
    plot_population_elevation(cur, conn)
    plt.clf()
    plot_city_review(cur, conn)
    plt.clf()
    plot_average_city_rating(cur, conn)
    plot.clf()
    plot_lat_long(cur,conn)

if __name__ == "__main__":
    main()