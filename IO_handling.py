import pandas
import re

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