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

# Load the NER(Named entity regognition) from LBNLP
#ner_model = load("ner")

# depth of the file path
# ie. "C:\path\to\extracted\data" would have a depth of 5
filepath_depth = 8

elems = []
cellCount = []
tagged_titles = []
# table titles
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

# # # extract the table title from the .json Adobe provides
# # ruby's note: first row in excel file
# def extractTitle(path):
#     global tagged_titles
#     global titles
#     global tags

#     titles_list = [] # store list of tags
#     data = json.load(open(path, encoding='UTF-8'))
#     # search through all the elements in the .json
#     for i in range(len(data['elements'])):
#         elem = data['elements'][i]
#         elem_path = elem['Path']
#         # find the elements that are tables
#         if re.match('^//Document/(.*?)Table(\[[0-9]+\])?$', elem_path):
#             title_elem = data['elements'][i - 1]
#             if 'Text' in title_elem:
#                 # store the title
#                 title = title_elem['Text']
#                 # tag the title and store it into titles_list
#                 flattened_tags = flatten(ner_model.tag_doc(title))
#                 titles_list.append(flattened_tags)
#             else:
#                 titles_list.append("")
#     for full_title in titles_list:
#         tagged_title = []
#         title = ""
#         tag = []
#         # iterate through each title
#         for word in full_title:
#             # if the tag is not o(other), store the word in the title in tagged title
#             if word[1] != 'O':
#                 tagged_title.append(word[0])
#                 tag.append(word[1])
#             # store the title itself
#             title += word[0] + " "
#         # add the tagged title, title, and tags to separate lists
#         tagged_titles.insert(0, tagged_title)
#         titles.insert(0, title)
#         tags.insert(0, tag)

def processTitle(xlsx_path):
    '''
    The first row of each xlsx file has the title
    '''
    return None, None

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

    # # retrieve the pdf title, tag, and tagged title
    # title = titles.pop()
    # tag = tags.pop()
    # tagged_title = tagged_titles.pop()

    # read the xlsx files using xlrd
    print('xlsx_path: ', xlsx_path)
    #wb = xlrd.open_workbook(xlsx_path)
    # sheet = wb.sheet_by_index(0)
    sheet = pd.read_excel(xlsx_path, sheet_name=0, index_col=None, header=None, engine='openpyxl')

    # count the total # of cells in the table
    #cellCount = [sheet.ncols] * sheet.nrows
    cellCount = [sheet.shape[1]] * sheet.shape[0]


    #check if the first row is the table title
    if len(cellCount) > 0:
        title = sheet.iloc[0,0]
        print('table title: ', title)
        tag, tagged_title = processTitle(title)

        # 'na' headers
        headers = ['na'] * sheet.shape[1]
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
# # # run the iterateDict which starts the process
# iterateDict()

# # inform user that the insertion is complete
# print("Insertion complete")
# # insert the data into MongoDB Atlas
# #db.ElsevierHEACreepPDFs.insert_many(elems)
# db.UncertaintyQuantification.insert_many(elems)


if __name__ == "__main__":
    iterateDict()
    #print(elems)
    print(len(elems))
    print('done!') 