from datetime import date
import pandas
import json
import requests
from bs4 import BeautifulSoup
import numpy


# Using the contents of a url page, scrape information and get provided JSON object
def getInventory(URL, targetBeltSize):
    
    responseDf = pandas.DataFrame()

    # For this specific website, there are some available json files
    JSON_URL = URL+".json"

    # Beautiful Soup, scrape json object about product information
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # If it detects a 404 page template, return an empty Df since there is nothing to gain from this page
    if(soup.find("body", {"class":"template-404"})!=None):
        return(responseDf)

    productName = json.loads(soup.find("script", type="application/ld+json").string)["name"]
    productData = json.loads(soup.main.find("script", type="application/ld+json").string)["offers"]

    print(productName)

    # dataframe with most information about products
    productDf= pandas.DataFrame(productData)

    # get additional information about product
    jsonDf = pandas.read_json(JSON_URL)
    itemDescriptionDf = pandas.DataFrame(jsonDf["product"]["variants"])

    # match two dataframes using stock keeping unit to identify products
    # add additional information about name and size
    productDf["size"] = numpy.where(itemDescriptionDf["sku"]==productDf["sku"],itemDescriptionDf["title"],numpy.nan)
    productDf["name"] = productName

    print(productName)
    print(productDf)

    # append information about certain products only if they are of the wanted size
    for i in targetBeltSize:
        responseDf = pandas.concat([responseDf.loc[:],productDf.loc[productDf["size"]==i]])

    # store only in stock products
    responseDf = responseDf.loc[responseDf["availability"].str.contains("InStock", case=False)]

    # display targeted products
    print(productName,"Notification List")
    print(responseDf, '\n')



    return(responseDf)

# Get the inventory of the products (given by a list of web links)
# Returns a dataframe of specific sized products that are in stock
def getAvailableStock(targetBeltSize, websiteList):
    
    # Dataframe that stores all relevant products that will be outputted to user
    notificationOutDf = pandas.DataFrame()


    # Append all targeted products into dataframe
    for i in websiteList:
        try:
            notificationOutDf = pandas.concat([notificationOutDf[:], getInventory(i, targetBeltSize)])
        except requests.exceptions.HTTPError as err:
            print(err)
            continue


    # Reset index for the new dataframe
    notificationOutDf.reset_index()

    # Display collected target products
    print("Final Notification Out List")
    print(notificationOutDf)

    # Return list of target products
    return(notificationOutDf)

# Output dataframe with related information in a readable format for a user
def outputMessage(inputDf):
    for index, i in inputDf.iterrows():
        print(i["name"],"\n", "Size:", i["size"], date.today(),"\n", "Link to item:","\n", i["url"],"\n")


    # REDUNDANT CODE: regex get all data inside "meta" js variable
    #allScripts = soup.find_all("script")
    # shopifyProductData = allScripts[36]
    #data = re.findall(r"({.*?});", shopifyProductData.string)
    #shopifyProductData = [i for i in data if i != "{}"]