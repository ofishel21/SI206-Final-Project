from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3
import os

def getRestaurantRatings(token):
    URL = "https://api.foursquare.com/v3/places/search?11=41.8781%2C-87.6298&categories=13000&fields=rating,name,stats&limit=50"


    headers = {
        "Accept": "application/json", 
        "Authorization": token
    }
    response = requests.get(url = URL, headers=headers)
    responses = json.loads(response.text)

    # resp_headers = response.headers
    # link = resp_headers['Link'][1:98]
    # second_responses = requests.get(url = link, headers = headers)
    # second_responses = json.loads(second_responses.text)

    return responses

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn  

def setUpRatingsTable(restaurantOutput, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Ratings (name TEXT PRIMARY KEY, rating INTEGER, total_ratings INTEGER)')
    for restaurant in restaurantOutput['results']:
        cur.execute('INSERT OR IGNORE INTO Ratings (name, rating, total_ratings) VALUES (?,?,?)', (restaurant['name'], restaurant['rating'], restaurant['stats']['total_ratings']))
    conn.commit()

def main():
    token = "fsq3XX8Bpj7/mc5IfDMBIMy3X8NXQszNg8FkBdFPlg3cHaw="
    restaurantOutput = getRestaurantRatings(token)
    cur, conn = setUpDatabase('Ratings.db')
    cur.execute('DROP TABLE IF EXISTS Ratings')
    setUpRatingsTable(restaurantOutput, cur, conn)
    dime = 10

if __name__ == '__main__':
    main()




    