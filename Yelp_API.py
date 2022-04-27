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

def tablesetup():
    cur.execute("CREATE TABLE IF NOT EXISTS RestaurantRatings (id INTEGER PRIMARY KEY, rating FLOAT, numberOfRatings INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS RestaurantName (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()

    name_lst = []
    rating_lst = []
    review_lst = []


    count = 0
    id_list = []
    id = 0
    for x in range(5):
        URL = f"https://api.yelp.com/v3/businesses/search?category=restaurants&location=AnnArbor&limit=25&offset={count}"
        header = {'Authorization' : 'Bearer oDX9DqPUXMG3neCXO79KRwmyzNDTdTsCpd54bUQJa4kSO_V_REvzcDF8XdYhQDwBPRK3MBavQe_Yw3TUVkFPSEgj7lKroNwdqgybOJOsdA2sYll7cQjByyCk32xPYnYx'}
        restaurant_lst = requests.get(url = URL, headers = header)
        restaurant_lst = restaurant_lst.text
        restaurant_dict = json.loads(restaurant_lst)
        count += 25
        businesses = restaurant_dict["businesses"]
        for business in businesses:
            name_lst.append(business['name'])
            rating_lst.append(business['rating'])
            review_lst.append(business['review_count'])
            id_list.append(id)
            id += 1



    count2 = 0
    for i in range(len(id_list)):
        if count2 == 25:
            break
        cur.execute("INSERT OR IGNORE INTO RestaurantName (id,name) VALUES (?,?)",(id_list[i],name_lst[i]))
        cur.execute("INSERT OR IGNORE INTO RestaurantRatings (id,rating, numberOfRatings) VALUES (?,?,?)",(id_list[i],rating_lst[i],review_lst[i]))
        if cur.rowcount == 1:
            count2 += 1
            print(name_lst[i])

    conn.commit()
    conn.close()

def PieChart():
    conn = sqlite3.connect(path+'/'+'206Project.db')
    cur = conn.cursor()
    cur.execute("SELECT rating FROM RestaurantRatings WHERE rating >= 3.5 AND rating < 4")
    three = len(cur.fetchall())

    cur.execute("SELECT rating FROM RestaurantRatings WHERE rating >= 4 AND rating < 4.5")
    four = len(cur.fetchall())

    cur.execute("SELECT rating FROM RestaurantRatings WHERE rating >= 4.5")
    five = len(cur.fetchall())

    distrubutiions = ['5.0 - 4.5', '4.5 - 4.0', '4.0 - 3.5']
    data = [three, four, five]

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


def main():
    tablesetup()
    #PieChart()
    


if __name__ == "__main__":
    main()