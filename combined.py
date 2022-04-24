import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import json

class getValue:
    data = []
    print(len(data))

j = 1

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'finaldb.db')
cur = conn.cursor()


def addtodb(n,r,rc):
    cur.execute(
        "INSERT INTO restaurants (restaurantName, rating, ratingCount) VALUES (?,?,?)", (n,r,rc))

def getname(name):
    try:
        if len(name) == 0:
            return "Name not defined"
        return name[3].text
    except IndexError:
        return "Name not defined"

def getRating(ratValue):
    if len(ratValue) == 0:
        return ""
    else:
        return ratValue[0].get("content")


for i in getValue.data:
    curl = "https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=Ann+Arbor%2C+MI" + i
    req = requests.get(curl)
    soup = BeautifulSoup(req.content, "html.parser")

    # get name of company
    cName = soup.find_all("span", {"itemprop": "name"})
    cName = getname(cName)

    # get company rating
    cRatV = soup.find_all("meta", {"itemprop": "ratingValue"})
    cRatV = getRating(cRatV)

    # get company rating count   
    cRatC = soup.find_all("meta", {"itemprop": "reviewCount"})
    cRatC = getRating(cRatC)


    addtodb(j, cName, cRatV, cRatC, curl)

    print("Acquired restaurant data")
    j += 1
    conn.commit()

cur.execute("CREATE TABLE IF NOT EXISTS RestaurantRatings (id INTEGER PRIMARY KEY, rating FLOAT, numberOfRatings INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS RestaurantName (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()

count = 0
id = 0
for x in range(4):
    URL = f"https://api.yelp.com/v3/businesses/search?category=restaurants&location=AnnArbor&limit=25&offset={count}"
    header = {'Authorization' : 'Bearer oDX9DqPUXMG3neCXO79KRwmyzNDTdTsCpd54bUQJa4kSO_V_REvzcDF8XdYhQDwBPRK3MBavQe_Yw3TUVkFPSEgj7lKroNwdqgybOJOsdA2sYll7cQjByyCk32xPYnYx'}
    restaurant_lst = requests.get(url = URL, headers = header)
    restaurant_lst = restaurant_lst.text
    restaurant_dict = json.loads(restaurant_lst)
    count += 25
    businesses = restaurant_dict["businesses"]
    for business in businesses:
        name = business['name']
        rating = business['rating']
        reviewNum = business['review_count']
        cur.execute("INSERT OR IGNORE INTO RestaurantName (id,name) VALUES (?,?)",(id,name))
        cur.execute("INSERT OR IGNORE INTO RestaurantRatings (id,rating, numberOfRatings) VALUES (?,?,?)",(id,rating,reviewNum))
        id += 1
        conn.commit()

from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3
import os


conn = sqlite3.connect("company.db")
cur = conn.cursor()

URL = "https://api.foursquare.com/v3/places/search?ll=41.8781%2C-87.6298&query=restaurant&categories=13000&fields=rating,name,stats&limit=50&radius=7000"

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3XX8Bpj7/mc5IfDMBIMy3X8NXQszNg8FkBdFPlg3cHaw="
}

response = requests.get(url = URL, headers=headers)
first_responses = (json.loads(response.text))


URL2 = "https://api.foursquare.com/v3/places/search?ll=41.8781%2C-87.6298&query=restaurant&categories=13000&fields=rating,name,stats&limit=50&radius=60000"

headers2 = {
    "Accept": "application/json",
    "Authorization": "fsq3XX8Bpj7/mc5IfDMBIMy3X8NXQszNg8FkBdFPlg3cHaw="
}

response2 = requests.get(url = URL2, headers=headers2)
first_responses2 = (json.loads(response2.text))


resp_headers = response.headers
link = resp_headers['Link'][1:76]
link = link+"41.8781%2C-87.6298&limit=50&fields=rating,name,stats&categories=13000&radius=20000&query=restaurant"
second_response = requests.get(url = link, headers = headers)
second_responses = json.loads(second_response.text)
first_responses = first_responses['results']
second_responses = second_responses['results']
first_responses2 = first_responses2['results']

restaurants1 = []
for rest in first_responses:
    restaurants1.append(rest)
    
restaurants2 = []
for rest in second_responses:
    restaurants2.append(rest)

restaurants3 = []
for rest in first_responses2:
    restaurants3.append(rest)




group1 = restaurants1[0:24]
group2= restaurants1[25:]
group3 = restaurants2[0:24]
group4= restaurants2[25:]
group5 = restaurants3[0:24]
group6= restaurants3[25:]



cur.execute('CREATE TABLE IF NOT EXISTS Ratings (name TEXT PRIMARY KEY, rating INTEGER, total_ratings INTEGER)')
for restaurant in group1:
   name = restaurant['name']
   rating = restaurant['rating']
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group2:
   name = restaurant['name']
   rating = restaurant['rating']
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group3:
   name = restaurant['name']
   rating = restaurant['rating']
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group4:
   name = restaurant['name']
   rating = restaurant['rating']
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group5:
   name = restaurant['name']
   rating = restaurant['rating']
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group6:
   name = restaurant['name']
   rating = restaurant['rating']
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))

conn.commit()
conn.close()
