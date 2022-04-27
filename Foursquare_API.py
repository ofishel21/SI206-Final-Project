import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'206Project.db')
cur = conn.cursor()

def APIsetup():

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

    restaurants = []
    for rest in first_responses:
        restaurants.append(rest)
    
    for rest in second_responses:
        restaurants.append(rest)

    for rest in first_responses2:
        restaurants.append(rest)

    name_lst = []
    rating_lst = []
    review_num = []



    cur.execute('CREATE TABLE IF NOT EXISTS Ratings (name TEXT PRIMARY KEY, rating FLOAT, total_ratings INTEGER)')

    id = 0
    idList = []
    for restaurant in restaurants:
        name_lst.append(restaurant['name'])
        rating = restaurant['rating']
        rating = rating/2
        rating_lst.append(rating)
        idList.append(id)
        review_num.append(restaurant['stats']['total_ratings'])
        id += 1


    count2 = 0
    for i in range(len(idList)):
        if count2 == 25:
            break
        cur.execute("INSERT OR IGNORE INTO Ratings (name,rating,total_ratings) VALUES (?,?,?)",(name_lst[i], rating_lst[i], review_num[i]))
        if cur.rowcount == 1:
            count2 += 1
            print(name_lst[i])
    
    
    conn.commit()
    conn.close()
    return(rating_lst)

def Histogram():
    data = {'Ratings': APIsetup()}
    df = pd.DataFrame(data)
    plot = sns.histplot(data = df)
    plot.set(xlabel='Ratings', ylabel='Frequency', title = 'Restaurant Count For Each Rating')
    plt.show()


            

def main():
    APIsetup()
    #Histogram()
    


if __name__ == "__main__":
    main()
