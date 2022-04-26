import requests
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

con = sqlite3.connect("restaurantdata.db")
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS restaurants (restaurantName TEXT, rating INTEGER, reviewCount INTEGER)')

def addtodb(n,r,rc):
    for i in range(len(n)):
        cursor.execute("INSERT INTO restaurants (restaurantName, rating, reviewCount) VALUES (?,?,?)", (n[i],r[i],rc[i]))
        con.commit()

    

name_list = []
rating_list = []
reviews_list = []


def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', class_ = 'hInfo vcard')

def names(businesses):
    for x in businesses:
        name = x.find('a', class_ = "url org").text
        name_list.append(name)
    return name_list


def ratings(businesses):
    for x in businesses:
        rating = x.find('span', class_ = 'rateVal').text
        rating_list.append(rating)
    return rating_list

def reviews(businesses):
    for x in businesses:
        try:
            bizReviews = x.find('div', class_ = 'reviewsWrap')
            reviews = bizReviews.find('a', class_ = 'reviewsQty').text[0]
        except:
            reviews = ''
        reviews_list.append(reviews)
    return reviews_list

for x in range(0,135,15):
    businesses = extract(f'https://www.merchantcircle.com/mi-ann-arbor/food-and-dining/restaurants?start={x}#hubResults')
    a = ratings(businesses)
    b = reviews(businesses)
    c = names(businesses)
    
addtodb(a,b,c)





con.close()
print("program finished")


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

#Data
data = {'Average Rating': [4.7,4.6,4.4,3.98,4.2,4,4.2]}
df = pd.DataFrame(data,columns=['Average Rating'], index = ['1','2','3','4','5','6','7'])


#Setting up Horizontal Bar Chart
df.plot.barh()


plt.title('Restaurant Rating Count vs Average Restaurant Rating')
plt.ylabel('Rating Count')
plt.xlabel('Average Rating')
plt.show()



