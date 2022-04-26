import sqlite3
import os
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'206Project.db')
cur = conn.cursor()

all_ratings = []
rubenratings = []
oliverratings = []
colinratings = []


cur.execute("SELECT RestaurantRatings.rating FROM RestaurantName JOIN RestaurantRatings ON RestaurantName.id = RestaurantRatings.id")
rubenRatings = cur.fetchall()
for rating in rubenRatings:
    all_ratings.append(rating[0])
    rubenratings.append(rating[0])


cur.execute("SELECT rating FROM Ratings")
oliverRatings = cur.fetchall()
for rating in oliverRatings:
    all_ratings.append(rating[0])
    oliverratings.append(rating[0])

cur.execute("SELECT rating FROM restaurants")
colinRatings = cur.fetchall()
for rating in colinRatings:
    all_ratings.append(rating[0])
    colinratings.append(rating[0])

sum = 0
for rating in all_ratings:
    sum += rating

average = sum / len(all_ratings)


##########
ratingCounts = []

cur.execute("SELECT numberOfRatings FROM RestaurantRatings")
rubenRatingCount = cur.fetchall()
for rating in rubenRatingCount:
    ratingCounts.append(rating[0])

cur.execute("SELECT total_ratings FROM Ratings")
oliverRatingCount = cur.fetchall()
for rating in oliverRatingCount:
    ratingCounts.append(rating[0])

cur.execute("SELECT reviewCount FROM restaurants")
colinRatingCount = cur.fetchall()
for rating in colinRatingCount:
    try:
        ratingCounts.append(int(rating[0]))
    except:
        continue

sum2 = 0
for count in ratingCounts:
    sum2 += count
averageCount = sum2 / len(ratingCounts)


plot = sns.jointplot(x= ratingCounts[0:150],y= all_ratings[0:150])
plot.fig.suptitle("Correlation of Rating Count with Rating")
plot.ax_joint.set_xlabel('Rating Count')
plot.ax_joint.set_ylabel('Rating')




with open("finalcsv.csv","w", newline = "") as file:
        writer = csv.writer(file, delimiter = ",")
        writer.writerow(['Average Rating', 'Total Rating Count', 'Average Rating Count'])
        writer.writerow([average, sum2, averageCount])
        file.close()

x = open('finalcsv.csv','r')
print(x.read())


data = {'Yelp': rubenratings[0:100], 'Foursquare': oliverratings[0:100], 'Merchant Circle': colinratings[0:100]}
df = pd.DataFrame(data)

#plot2 = sns.boxplot(data = df)
#plot2.set(xlabel = 'APIs/Websites', ylabel = 'Ratings', title = "Distribution of Ratings Across APIs/Websites")
plt.show()

        
