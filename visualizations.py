import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

def dbSetup(db_name):
    ''' Takes in database name (reastaurants.db) as a parameter and returns the connection and curser for the database'''
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    return cur, conn

def bar_1(cur):
    
#implement code here for blue bar chart

def bar_2(cur):

#implement code here for green bar chart


def pie(cur):
    
#implement code here for pie chart


def scatter(cur):

#implement code here for scatter plot

def box(cur):
    ''' Takes in the database curser as a parameter. Selects the cryptocurrency name and tweet count 
        to create a bar chart with the cryptocurrency on the x axis and the tweet count on the y axis'''
    

#implement code here for box and wisker



def main():

    cur,conn = dbSetup('restaurants.db') 
    bar_1(cur)
    bar_2(cur)
    pie(cur)
    scatter(cur)
    box(cur)

    conn.close()

if __name__ == "__main__":
    main()
