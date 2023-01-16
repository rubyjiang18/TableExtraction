
# imports
import json
import os
import re
import xlrd
import pprint
import pandas as pd

from pymongo import MongoClient
#from lbnlp.models.load.matscholar_2020v1 import load

mergeCol = 0

# Path to the folders Adobe's API Extracted
#folderPath = r'C:\Users\Jason\OneDrive\Documents\pdfservices-java-sdk-samples-master\output\ElsevierHEACreepPDFs\ExtractedData'
folderPath = r'/Users/rubyjiang/Desktop/HTMDEC/table_extractor/tableextractor/test/ExtractedData'

# cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

# Link to the MongoDB cluster
cluster = "mongodb://table_extraction:vlldc3JRnDG2DvW3@cluster0-shard-00-00.afvrd.mongodb.net:27017,cluster0-shard-00-01.afvrd.mongodb.net:27017,cluster0-shard-00-02.afvrd.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-12bs5c-shard-0&authSource=admin&retryWrites=true&w=majority"

# Setup MongoDB
client = MongoClient(cluster)

# Database name (leave unchanged)
db = client.data

# delete
db.UncertaintyQuantification.delete_many({})
