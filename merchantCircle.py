import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import matplotlib.pyplot as plt
import pandas as pd

def setUpDatabase(db):
    '''takes in database name (restaurants.db) as parameter and returns the connection and curser for the database'''
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn

def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', class_ = 'hInfo vcard')


def merchantCircleTable(businesses, cur, conn):
    count = 0
    name_list = []
    rating_list = []
    reviews_list = []
    for x in businesses:
        name = x.find('a', class_ = "url org").text
        name_list.append(name)
        rating = x.find('span', class_ = 'rateVal').text
        rating_list.append(rating)
        try:
            bizReviews = x.find('div', class_ = 'reviewsWrap')
            reviews = bizReviews.find('a', class_ = 'reviewsQty').text[0]
        except:
            reviews = ''
        reviews_list.append(reviews)

    cur.execute('CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY, restaurantName TEXT, rating INTEGER, reviewCount INTEGER)')

    count = 0 
    for i in range(len(businesses)):
        if count == 25:
            break
        cur.execute("INSERT INTO restaurants (restaurantName, rating, reviewCount) VALUES (?,?,?)", (name_list[i],rating_list[i],reviews_list[i]))
        if cur.rowcount == 1:
            count += 1

    conn.commit()

def barhr():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'206Project.db')
    cur = conn.cursor()

    #Getting Data
    cur.execute("SELECT reviewCount FROM restaurants WHERE reviewCount = 1")
    one = len(cur.fetchall())

    cur.execute("SELECT reviewCount FROM restaurants WHERE reviewCount = 2")
    two = len(cur.fetchall())

    cur.execute("SELECT reviewCount FROM restaurants WHERE reviewCount = 3")
    three = len(cur.fetchall())

    cur.execute("SELECT reviewCount FROM restaurants WHERE reviewCount = 4")
    four = len(cur.fetchall())

    cur.execute("SELECT reviewCount FROM restaurants WHERE reviewCount >= 5")
    above = len(cur.fetchall())

    data = {'Restaurant Count': [one, two, three, four, above]}
    df = pd.DataFrame(data,columns=['Restaurant Count'], index = ['1','2','3','4','Above 5'])


    # Visualization

    #Font
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Helvetica'

    # set the style of the axes and the text color
    plt.rcParams['axes.edgecolor']='#333F4B'
    plt.rcParams['axes.linewidth']=0.8
    plt.rcParams['xtick.color']='#333F4B'
    plt.rcParams['ytick.color']='#333F4B'
    plt.rcParams['text.color']='#333F4B'

    #Setting up Horizontal Bar Chart
    df.plot.barh()


    plt.title('Amount of Restaurants With Specific Rating Counts')
    plt.ylabel('Rating Count')
    plt.xlabel('Amount of Restaurants')
    plt.show()



def main():
    cur, conn = setUpDatabase('206Project.db')
    for x in range(0,135,15):
        businesses = extract(f'https://www.merchantcircle.com/mi-ann-arbor/food-and-dining/restaurants?start={x}#hubResults')
    merchantCircleTable(businesses, cur, conn)


    #Uncomment barh() below when you want to see the visualization
    # barhr()

    conn.close()
    print("program finished")

if __name__ == "__main__":
    main()



