import requests
from bs4 import BeautifulSoup
import re
import json
from parsel import Selector
import pandas
import numpy
from datetime import date
import fbchat
from getpass import getpass

from os import environ

from dotenv import load_dotenv
load_dotenv()

targetBeltSize = ['M','L']

# Using the contents of a url page, scrape information and get provided JSON object
def getInventory(URL, targetBeltSize):
    
    responseDf = pandas.DataFrame()

    JSON_URL = URL+".json"

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    productName = json.loads(soup.find("script", type="application/ld+json").string)["name"]

    productData = json.loads(soup.main.find("script", type="application/ld+json").string)["offers"]

    productDf= pandas.DataFrame(productData)

    allScripts = soup.find_all("script")

    shopifyProductData = allScripts[36]

    # REDUNDANT CODE: regex get all data inside "meta" js variable
    #data = re.findall(r"({.*?});", shopifyProductData.string)
    #shopifyProductData = [i for i in data if i != "{}"]

    jsonDf = pandas.read_json(JSON_URL)
    itemDescriptionDf = pandas.DataFrame(jsonDf["product"]["variants"])

    productDf["size"] = numpy.where(itemDescriptionDf["sku"]==productDf["sku"],itemDescriptionDf["title"],numpy.nan)
    productDf["name"] = productName

    print(productName)
    print(productDf)

    for i in targetBeltSize:
        responseDf = pandas.concat([responseDf.loc[:],productDf.loc[productDf["size"]==i]])

    responseDf = responseDf.loc[responseDf["availability"].str.contains("InStock", case=False)]

    print(productName,"Notification List")
    print(responseDf, '\n')

    return(responseDf)

# Get lists of urls from url_list.txt
def getListURL():
    url_file = open('url_list.txt','r')
    urlData = url_file.read()
  
    urlList = urlData.split("\n")
    url_file.close()

    return urlList

# Get the inventory of the products given by the lists of web links
def scrapeList(targetBeltSize):
    websiteList = getListURL()

    # Dataframe that stores all relevant products
    notificationOutDf = pandas.DataFrame()

    for i in websiteList:
        notificationOutDf = pandas.concat([notificationOutDf[:],getInventory(i ,targetBeltSize)])
    notificationOutDf.reset_index()

    print("Final Notification Out List")
    print(notificationOutDf)

    return(notificationOutDf)


def outputMessage(notificationOutDf):
    for index, i in notificationOutDf.iterrows():
        print(i["name"],"\n", "Size:", i["size"], date.today(),"\n", "Link to belt:","\n", i["url"])

outputMessage(scrapeList(targetBeltSize))

