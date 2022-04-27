import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'206Project.db')
cur = conn.cursor()

idList = []
nameList = []

cur.execute("SELECT RestaurantName.id FROM RestaurantName JOIN restaurants ON RestaurantName.name = restaurants.restaurantName")
ids = cur.fetchall()
for id in ids:
    if id[0] not in idList:
        idList.append(id[0])

cur.execute("SELECT id FROM RestaurantName JOIN Ratings ON RestaurantName.name = Ratings.name")
ids2 = cur.fetchall()
for id in ids2:
    if id[0] not in idList:
        idList.append(id[0])

idList = tuple(idList)

cur.execute("SELECT name FROM RestaurantName WHERE RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ?", idList)
names = cur.fetchall()
for name in names:
    if name[0] not in nameList:
        nameList.append(name[0])

cur.execute("SELECT name FROM Ratings JOIN restaurants WHERE Ratings.name = restaurants.restaurantName")
nameList2 = []
sameName = cur.fetchall()
for name in sameName:
    if name[0] not in nameList2:
        nameList2.append(name[0])
try:
    cur.execute("DELETE FROM RestaurantName WHERE RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ? OR RestaurantName.id = ?", idList)
except:
    print('0')
try:
    cur.execute("DELETE FROM RestaurantRatings WHERE RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ? OR RestaurantRatings.id = ?", idList)
except:
   print('0')
try:
    cur.execute("DELETE FROM restaurants WHERE restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ?", nameList)
except:
    print('0')
try:
    cur.execute("DELETE FROM Ratings WHERE Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ?", nameList)
except:
    print('0')
try:
    cur.execute("DELETE FROM restaurants WHERE restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ? OR restaurants.restaurantName = ?", nameList2)
except:
   print('0')
try:
    cur.execute("DELETE FROM Ratings WHERE Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ? OR Ratings.name = ?", nameList2)
except:
    print('0')
conn.commit()
conn.close()