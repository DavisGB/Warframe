# Import libraries
import requests
import urllib.request
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Set the URL you want to webscrape from
url = 'https://warframe.market'

# Connect to the URL
response = requests.get(url)
# Parse HTML and save to BeautifulSoup object¶
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Warframe Market Data-e135d53d9979.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Warframe Market Data")
soup = BeautifulSoup(response.text, "html.parser")
selldivisionwtag = soup.find('script',id = 'application-state')
selldivisionrtag1 = str(selldivisionwtag).replace('<script id="application-state" type="application/json">','')
selldivision = str(selldivisionrtag1).replace('</script>','')
selldivisionjson = json.loads(selldivision)
for currentorder in selldivisionjson['payload']['sell_orders']:
    currentorderurl = "https://warframe.market/items/" + currentorder["item"]["url_name"]
    sellorderpage = requests.get(currentorderurl)
    sellordersoup = BeautifulSoup(sellorderpage.text, "html.parser")
    sellorderswtag = sellordersoup.find('script',id = 'application-state')
    sellordersrtag1 = str(sellorderswtag).replace('<script id="application-state" type="application/json">','')
    sellorders = str(sellordersrtag1).replace('</script>','')
    sellordersjson = json.loads(sellorders)
    print(currentorder['item']['pt']['item_name'])
    try:
        currentworksheet = sheet.worksheet(currentorder['item']['pt']['item_name'])
    except:
        currentworksheet = sheet.add_worksheet(title=currentorder['item']['pt']['item_name'], rows="100", cols="20")
        currentworksheet.update('A4','Lowest Sell Order')
        currentworksheet.update('C4','Highest Buy Order')
        currentworksheet.update('A7','OnlineSellOrders')
        currentworksheet.update('C7','SellPrice')
        currentworksheet.update('E7','Quantity')
        currentworksheet.update('G7','OnlineBuyOrders')
        currentworksheet.update('I7','BuyPrice')
        currentworksheet.update('K7','Quantity')
        currentworksheet.update('B4','0')
        currentworksheet.update_cell(4,2,'0')
    cheapestsellorder = currentworksheet.cell(4,2).value
    if currentorder['user']['status'] == 'ingame':
        if cheapestsellorder == '0':
            currentworksheet.update('B4',currentorder['platinum'])
        else:
            if int(float(cheapestsellorder)) > int(currentorder['platinum']):
                  currentworksheet.update('B4',currentorder['platinum'])
    i = 1
    for currentsellorderinpage in sellordersjson['payload']['orders']:
        if ((currentsellorderinpage['user']['status'] == 'ingame') and (currentsellorderinpage['order_type'] == 'sell') ):
            if int(currentsellorderinpage['platinum']) < int((float(cheapestsellorder))):
                currentworksheet.update('B4',currentsellorderinpage['platinum'])
        sellcell = currentworksheet.find('SellPrice')
        currentworksheet.update_cell(sellcell.row + i,sellcell.col,currentsellorderinpage['platinum'])
        currentworksheet.update_cell(sellcell.row + i,sellcell.col+2,currentsellorderinpage['quantity'])
        i = i + 1
    print('price' , currentorder['platinum'] )
    print('quantity' , currentorder['quantity'] )
    print('\n')
    time.sleep(1)


    

'''
orderurl = 'https://warframe.market/items/rift_torrent'
sellorderpage = requests.get(orderurl)
sellordersoup = BeautifulSoup(sellorderpage.text, "html.parser")
sellorderswtag = sellordersoup.find('script',id = 'application-state')
sellordersrtag1 = str(sellorderswtag).replace('<script id="application-state" type="application/json">','')
sellorders = str(sellordersrtag1).replace('</script>','')
sellordersjson = json.loads(sellorders)
print(orderurl)
for currentorder in sellordersjson['payload']['orders']:
    if currentorder['order_type'] == 'sell':
        print('mod rank' , currentorder['mod_rank'])
        print('price' , currentorder['platinum'] )
        print('quantity' , currentorder['quantity'] )
        print('\n')
'''




'''
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Warframe Market Data-e135d53d9979.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Warframe Market Data")
try:
    currentworksheet = sheet.worksheet("Rift Torrent")
except:
    currentworksheet = sheet.add_worksheet(title="Rift Torrent", rows="100", cols="20")
'''    


