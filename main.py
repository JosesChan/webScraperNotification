import pandas
from IO_handling import getListURL, exportCSV
from data_handling import getAvailableStock, outputMessage

from getpass import getpass

from os import environ

targetBeltSize = ['M','L']

productPages = getListURL()

if(productPages!=None):
    currentStock = getAvailableStock(targetBeltSize, productPages)

    outputMessage(currentStock)

    exportCSV(currentStock)
else:
    print("Pages cant be retrieved")