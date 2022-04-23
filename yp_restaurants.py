import requests
from bs4 import BeautifulSoup
import sqlite3
import getValue

j = 1

con = sqlite3.connect("companydata.db")
cursor = con.cursor()


def addtodb(n,r,rc):
    cursor.execute(
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


for i in getvalue.data:
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
    con.commit()

con.close()
print("program finished")