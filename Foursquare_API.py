import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect("SIFinalDB.db")
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



cur.execute('CREATE TABLE IF NOT EXISTS Ratings (name TEXT PRIMARY KEY, rating FLOAT, total_ratings INTEGER)')
for restaurant in group1:
   name = restaurant['name']
   rating = restaurant['rating']
   rating = rating/2
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group2:
   name = restaurant['name']
   rating = restaurant['rating']
   rating = rating/2
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group3:
   name = restaurant['name']
   rating = restaurant['rating']
   rating = rating/2
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group4:
   name = restaurant['name']
   rating = restaurant['rating']
   rating = rating/2
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group5:
   name = restaurant['name']
   rating = restaurant['rating']
   rating = rating/2
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))
for restaurant in group6:
   name = restaurant['name']
   rating = restaurant['rating']
   rating = rating/2
   totratings = restaurant['stats']['total_ratings']
   cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (name, rating, totratings))

conn.commit()

conn.close()

# Creating categories
distrubutiions = ['5.0 - 4.5', '4.5 - 4.0', '4.0 - 3.5']
 
data = [39, 44, 17]
 
 
# Creating explode data
explode = (0.05, 0.1, 0.0)
 
# Creating color parameters
colors = ( "orange", "cyan", "indigo")
 
# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "blue" }
 
# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} Restaurants)".format(pct, absolute)
 
# Creating plot
fig, ax = plt.subplots(figsize =(10, 7))
wedges, texts, autotexts = ax.pie(data,
                                  autopct = lambda pct: func(pct, data),
                                  explode = explode,
                                  labels = distrubutiions,
                                  shadow = True,
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color = "red"))
 
# Adding legend
ax.legend(wedges, distrubutiions,
          title = "Rating Distributions",
          loc = "center left",
          bbox_to_anchor =(1, 0, 0.5, 1))
 
plt.setp(autotexts, size = 8, weight = "bold")
plt.title('Restaurant Rating Distributions', fontsize = 12, weight = "bold")
 
# show plot
plt.show()