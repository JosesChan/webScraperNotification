import pandas
import re
import os
from fbchat import Client
from fbchat.models import *


# try:

#     client = Client('<email>', '<password>')

# except:
#     print("Error getting FB details, please edit to ensure they're correct")



print(os.environ.get('FB_USER'))


# Get lists of urls from url_list.txt
def getListURL():
    url_file = open('url_list.txt','r')
    urlData = url_file.read()
  
    # Split urls by lines
    urlList = urlData.split("\n")
    url_file.close()

    # Return content without empty lines
    return filter(lambda x: not re.match(r'^\s*$', x), urlList)

# export the dataframe as CSV
def exportCSV(exportDataframe):
    exportDataframe.to_csv("Available Stock.csv")