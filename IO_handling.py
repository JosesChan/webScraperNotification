import pandas

# Get lists of urls from url_list.txt
def getListURL():
    url_file = open('url_list.txt','r')
    urlData = url_file.read()
  
    urlList = urlData.split("\n")
    url_file.close()

    return urlList

# export the dataframe as CSV
def exportCSV(exportDataframe):
    exportDataframe.to_csv("Available Stock.csv")