# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 08:51:33 2016

@author: gus
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from random import randint
import csv

rav4_url = "http://www.encuentra24.com/panama-es/autos-usados#search=keyword.Rav4|number.50&page=1"
url = r"http://www.encuentra24.com/panama-es/autos-usados#search=number.50&page=1"
url_2 = "http://www.encuentra24.com/panama-es/autos-usados.2"
url_13 = "http://www.encuentra24.com/panama-es/autos-usados.13"
base_url = "http://www.encuentra24.com/panama-es/autos-usados"
rav4_id = '5456684'
tag = 'article'
class_id = "ann-box-teaser ann-box-teaser-auto regular feat-normal no-color"



def get_cars():
    with open("mydata.csv", "ab") as w:
        writer = csv.DictWriter(w, ["name", "price", "descrip", "year", "mileage", "post"])
        writer.writeheader()
        myData = []    
        for i in range(968, 1100):
        #for i in range(1100, 1104):
            url = base_url + "." + str(i)
            print url
            response = requests.get(url)
            print response
            soup = BeautifulSoup(response.text)
            #soup = BeautifulSoup(open("sample.html"))
            for car in soup.find_all("article", {"class": "ann-box-teaser"}):
                myCar = {}
                for x in car.find_all("div", {"class": "ann-box-details"}):
                    name = x.find("strong").text
                    price = x.find("span", {"class": "ann-price"}).text
                    descrip = x.find("span", {"class": "ann-box-desc"}).text
                    try:
                        myCar['name'] = name.encode("ascii", "ignore")
                    except IndexError:
                        print "No name {}".format(str(i))
                    try:
                        myCar['price'] = price.encode("ascii", "ignore")
                    except IndexError:
                        print "No price {}".format(str(i))
                    try:
                        myCar['descrip'] = descrip.encode("ascii", "ignore").strip("\n")
                    except IndexError:
                        print "No descrip {}".format(str(i))
                for a in car.find_all("div", {"class": "ann-box-info"}):
                    vals = a.find_all("span", {"class": "value"})
                    try:
                        myCar['year'] = vals[0].text.encode("ascii", "ignore")
                    except IndexError:
                        print "No year {}".format(str(i))
                    try:
                        myCar['mileage'] = vals[1].text.encode("ascii", "ignore")
                    except IndexError:
                        print "No mileage {}".format(str(i))
                """
                for y in car.find_all("li", {"class": "hide-on-hover-1024"}):
                    mileage = y.find("span", {"class": "value"}).text.encode("ascii", "ignore")
                    myCar['mileage'] = mileage
                """
                for z in car.find_all("li", {"class": "hide-on-hover ann-box-hilight-time"}):
                    post = z.find("span", {"class": "value"}).text.encode("ascii", "ignore")
                    myCar['post'] = post
                writer.writerow(myCar)
                myData.append(myCar)
                time.sleep(randint(1,4))
                
        return myData

def get_file(myfile):
    myData = []    
    soup = BeautifulSoup(open(myfile))
    for car in soup.find_all("article", {"class": "ann-box-teaser"}):
        myCar = {}
        for x in car.find_all("div", {"class": "ann-box-details"}):
            name = x.find("strong").text
            price = x.find("span", {"class": "ann-price"}).text
            descrip = x.find("span", {"class": "ann-box-desc"}).text
            myCar['name'] = name.encode("ascii", "ignore")
            myCar['price'] = price.encode("ascii", "ignore")
            myCar['descrip'] = descrip.encode("ascii", "ignore").strip("\n")
        for a in car.find_all("div", {"class": "ann-box-info"}):
            vals = a.find_all("span", {"class": "value"})
            myCar['year'] = vals[0].text.encode("ascii", "ignore")
            myCar['mileage'] = vals[1].text.encode("ascii", "ignore")
        for z in car.find_all("li", {"class": "hide-on-hover ann-box-hilight-time"}):
            post = z.find("span", {"class": "value"}).text.encode("ascii", "ignore")
            myCar['post'] = post
        myData.append(myCar)
        time.sleep(randint(1,4))
    return myData
    

    
if __name__ == '__main__':   
    myData = get_cars()
    df = pd.DataFrame(myData)
    df.to_csv("encuentro_data2.csv")
    #myData = get_file("sample13.html")
    

    """
    response = requests.get(url_13)
    soup = BeautifulSoup(response.text)
    
    with open("sample13.html", "wb") as w:
        w.write(response.content)
    """
