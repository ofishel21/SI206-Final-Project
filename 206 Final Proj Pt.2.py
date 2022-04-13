from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'206FinalPractice.db')
cur = conn.cursor()

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

        