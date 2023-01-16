"""
Updated Version from Jason's procTable.
Script to extract the table data and metadata from the xlsx and (no .json file) files XML extraction tool provides.
Inserts the extracted data into MongoDB Atlas for easy cloud access.
"""

# imports
import json
import os
import re
import xlrd
import pprint
import pandas as pd

from pymongo import MongoClient
from lbnlp.models.load.matscholar_2020v1 import load

mergeCol = 0

# Path to the folders Adobe's API Extracted
#folderPath = r'C:\Users\Jason\OneDrive\Documents\pdfservices-java-sdk-samples-master\output\ElsevierHEACreepPDFs\ExtractedData'
folderPath = r'/Users/rubyjiang/Desktop/xml_table_extractor_fake/tableextractor/test/ExtractedData'

# cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

# Link to the MongoDB cluster
cluster = "mongodb://table_extraction:vlldc3JRnDG2DvW3@cluster0-shard-00-00.afvrd.mongodb.net:27017,cluster0-shard-00-01.afvrd.mongodb.net:27017,cluster0-shard-00-02.afvrd.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-12bs5c-shard-0&authSource=admin&retryWrites=true&w=majority"

# Setup MongoDB
client = MongoClient(cluster)

# Database name (leave unchanged)
db = client.data

# Load the NER(Named entity regognition) from LBNLP
ner_model = load("ner")
print('model_loaded!')

# depth of the file path
# ie. "C:\path\to\extracted\data" would have a depth of 5
filepath_depth = 8

elems = []
cellCount = []
tagged_titles = []
titles = []
tags = []

# If text is a number, convert it to a number
def atoi(text):
    return int(text) if text.isdigit() else text

"""
Used to sort the files in numerical order
When sorting a string, sort will naturally sort in the order:
test1
test11
test12
test2
test3
...
test9
"""
def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

# Print the elements in a MongoDB database
def display(cursor):
    for document in cursor:
        print()
        pprint(document)

# flatten a multi dimensional list into a 1D list
# IE: [[[1, 2], 3], [4, 5]] -> [1, 2, 3, 4, 5]
def flatten(tags):
    flattened_tags = []
    for sentence in tags:
        flattened_tags.extend(sentence)
    return flattened_tags

def processTitle(title):
    '''
    The first row of each xlsx file has the title
    '''
    flattened_tags = flatten(ner_model.tag_doc(title))
    tags = []
    tagged_titles = []
    # raw_tag example ('crystallographic', 'B-PRO')
    for raw_tags in flattened_tags:
        if raw_tags[1] != 'O':
            tag = raw_tags[1]
            tagged_title = raw_tags[0]
            tags.append(tag)
            tagged_titles.append(tagged_title)
    return tags, tagged_titles

# Extract data from xlsx files
def extractTable(xlsx_path, subdir):
    global elems
    global cellCount
    global titles
    global tagged_titles
    global tags
    # get the title of the PDF
    path_list = subdir.split("/")
    pdf_title = path_list[len(path_list)-2]
    print('pdf_title: ', pdf_title)

    # read the xlsx files using xlrd
    print('xlsx_path: ', xlsx_path)
    #wb = xlrd.open_workbook(xlsx_path)
    # sheet = wb.sheet_by_index(0)
    sheet = pd.read_excel(xlsx_path, sheet_name=0, index_col=None, header=None, engine='openpyxl')

    # count the total # of cells in the table
    #cellCount = [sheet.ncols] * sheet.nrows
    cellCount = [sheet.shape[1]] * sheet.shape[0]

    #first row is the table title
    if len(cellCount) > 0:
        title = sheet.iloc[0,0]
        print('table title: ', title)
        tag, tagged_title = processTitle(title)

        # # 'na' headers
        # headers = ['na'] * sheet.shape[1]
        # we assume second row is header and all the rows down there are table contents
        headers = sheet.iloc[1].to_list() # second row
        header_length = len(headers)
        if header_length < sheet.shape[1]:
            for i in range(sheet.shape[1] - header_length):
                headers.append("na" + str(i))
        print("headers: ")
        print(headers)

        # insert the rest of the data in the table
        for row in range(1, sheet.shape[0]):
            table = [] # a row of data
            # for each cell, create a key-value pair with the header above it and the value of the cell
            for col in range(sheet.shape[1]):
                #d = {'name': headers[col], 'value': ''.join(unmergedValue(row, col, sheet).splitlines())}  
                d = {'name': headers[col], 'value': sheet.iloc[row, col]}
                table.append(d)
            # add additional metadata to the row including the table title, tagged title, tags, and pdf title
            elems.append({'body': table, 'title': title, 'tagged_title': tagged_title, 'tags': tag, 'pdf_title': pdf_title})

# iterate through the folder with the extracted data from Adobe
def iterateDict():
    
    for subdir, dirs, files in os.walk(folderPath):
        print('sudir', subdir)
        print('dirs', dirs)
        # sort the xlsx files by their number so the table title extracted from the .json is correct
        for file in sorted(files, key=natural_keys):
            print(file)
            #if the file ends with xlsx, run extractTable
            if file.endswith('.xlsx') and '~$' not in file:
                xlsx_path = os.path.join(subdir, file)
                extractTable(xlsx_path, subdir)

###### Insert all elems into DB   
# # run the iterateDict which starts the process
iterateDict()

# inform user that the insertion is complete
print("Insertion complete")
# insert the data into MongoDB Atlas
#db.ElsevierHEACreepPDFs.insert_many(elems)
db.UncertaintyQuantification.insert_many(elems)


# if __name__ == "__main__":
#     iterateDict()
#     #print(elems)
#     print(len(elems))
#     print('done!') 