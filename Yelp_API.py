from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'206Project.db')
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

# Creating dataset
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
conn.close()
        