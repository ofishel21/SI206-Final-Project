import requests
from bs4 import BeautifulSoup
import sqlite3

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



