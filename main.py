import pandas
from IO_handling import getListURL, exportCSV
from data_handling import getAvailableStock, outputMessage
from schedule_handling import scheduleProgram
from getpass import getpass
from os import environ

def programRun():
    targetBeltSize = ['M','L']

    productPages = getListURL()
    if(productPages!=None):
        currentStock = getAvailableStock(targetBeltSize, productPages)
        outputMessage(currentStock)
        exportCSV(currentStock)
    else:
        print("Pages cant be retrieved")
    
scheduleProgram(programRun)