# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 09:10:28 2022

@author: fardad
"""
from bs4 import BeautifulSoup
import requests
import re
import mysql.connector

ch1 = True
while ch1:
    q1 = input("Is this your first run of data-fetcher?(y/n): ").lower()
    if q1 == 'y' or q1 == 'n':
        ch1 = False
    else:
        print("Wrong input try again!!!")
if q1 == 'y':
    q1 = True
else:
    q1 = False

if q1 == True:
    pageStart = 1
else: 
    pageStart = int(input("Which page do you left of?  "))

databaseName = input("Enter your database name: ")
databaseUser = input("Enter your database username: ")
dataPass = input("Enter your database password: ")
if q1 == True:
    print('''
      Your Table Must Have 4 Columns:
          Column 1 Should Be varchar(255) For Car Name
          Column 2 Should Be int For Car Year
          Column 3 Should Be int For Car Usage
          Column 4 Should Be int For Car Price
          ''')
tableName = input("Enter your table name: ")

    
cnx = mysql.connector.connect(user=databaseUser, password=dataPass,
                              host='127.0.0.1', database=databaseName)
cursor = cnx.cursor()
for x in range(pageStart,334):
    print(f'page counter: {x}')
    r = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/?page={x}')
    ercode = r
    q2 = True
    if re.search(r'<\w* \[(200)\]>',str(ercode)) == None:
        q2 = False
        break
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('div', attrs = {'data-test' : 'vehicleMileage'})
    PriceResults = soup.find_all('div',
                                 attrs = {'data-test' : 'vehicleCardPricingBlockPrice'})
    nameResults = soup.find_all('span',
                                attrs = {'class' : 'vehicle-header-make-model text-truncate'})
    yearResults = soup.find_all('span',
                                attrs = {'class' : 'vehicle-card-year font-size-1'})
    
    usageList = []
    priceList = []
    nameList = []
    yearList = []

    
    for item in results:
        temp=re.sub("^<.*?><.*?>", "", item.text)
        temp=re.sub(r"[^\d]", "", temp)
        usageList.append(int(temp))
    for price in PriceResults:
        temp_2=re.sub("^<.*?><.*?>", "", price.text)
        temp_2=re.sub(r"[^\d]", "", temp_2)
        priceList.append(int(temp_2))
    for name in nameResults:
        temp_3=re.sub("^<.*?><.*?>", "", name.text)
        nameList.append(temp_3)
    for year in yearResults:
        temp_4=re.sub("^<.*?><.*?>", "", year.text)
        yearList.append(int(temp_4))
        
    for i,j,k,l in zip(nameList, yearList, usageList, priceList):
        cursor.execute(f"INSERT INTO {tableName} VALUES ('{i}', '{j}', '{k}', '{l}')")
        
    cnx.commit()
if q2 == False:
        print(f"Ran into a network problem please try again at page{x}")
        input("Press Enter to exit")    
if x == 334:
    print("Reading data from Truecar website is done now!!")
cnx.close()
