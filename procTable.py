<<<<<<< HEAD
"""
Script to extract the table data and metadata from the xlsx and .json files Adobe's pdf extraction api provides.
Inserts the extracted data into MongoDB Atlas for easy cloud access.
"""

# imports
=======
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
import json
import os
import re
import xlrd
import pprint

from pymongo import MongoClient
from lbnlp.models.load.matscholar_2020v1 import load

mergeCol = 0

<<<<<<< HEAD
# Path to the folders Adobe's API Extracted
folderPath = r'C:\Users\Jason\OneDrive\Documents\pdfservices-java-sdk-samples-master\output\ElsevierHEACreepPDFs\ExtractedData'

# cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

# Link to the MongoDB cluster
cluster = "mongodb://table_extraction:vlldc3JRnDG2DvW3@cluster0-shard-00-00.afvrd.mongodb.net:27017,cluster0-shard-00-01.afvrd.mongodb.net:27017,cluster0-shard-00-02.afvrd.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-12bs5c-shard-0&authSource=admin&retryWrites=true&w=majority"

# Setup MongoDB
client = MongoClient(cluster)

# Database name (leave unchanged)
db = client.data

# Load the NER(Named entity regognition) from LBNLP
ner_model = load("ner")

# depth of the file path
# ie. "C:\path\to\extracted\data" would have a depth of 5
filepath_depth = 8

=======
loc = "fileoutpart0.xlsx"
folderPath = r'C:\Users\Jason\Documents\pdftools\adobe-dc-pdf-services-sdk-java-samples\output\ExtractedData'
cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
client = MongoClient(cluster)
db = client.data

ner_model = load("ner")

>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
elems = []
cellCount = []
tagged_titles = []
titles = []
tags = []

<<<<<<< HEAD
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
=======
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
def display(cursor):
    for document in cursor:
        print()
        pprint(document)

<<<<<<< HEAD
# Get the value of a merged cell in a xlsx file
def unmergedValue(rowx, colx, thesheet):
    # iterate through the merged cells
    for crange in thesheet.merged_cells:
        # rl -> lower row bound of the merged cell
        # rhi -> upper row bound of the merged cell
        # clow -> lower column bound of the merged cell
        # chi -> upper row bound of the merged cell
        rlo, rhi, clo, chi = crange
        # if the merged cell was found, return it
=======

def unmergedValue(rowx, colx, thesheet):
    for crange in thesheet.merged_cells:
        rlo, rhi, clo, chi = crange
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return thesheet.cell_value(rlo, clo)
    return thesheet.cell_value(rowx, colx)

<<<<<<< HEAD
# Detect which rows in a table are the header
def detectHeaders(sheet, start):
    header_height = 0
    global cellCount
    # count the number of columns in each row
    for crange in sheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if start == 1:
            continue
        for row in range(rlo, rhi):
            cellCount[row] -= chi - clo
    # find the max number of columns
    maxCol = max(cellCount)
    # set the first header to the row after the first row with the most number of columns
=======

def detectHeaders(sheet):
    header_height = 0
    global cellCount
    for crange in sheet.merged_cells:
        rlo, rhi, clo, chi = crange
        for row in range(rlo, rhi):
            cellCount[row] -= chi - clo
    maxCol = max(cellCount)
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
    for i in range(len(cellCount)):
        if cellCount[i] == maxCol:
            header_height = i + 1
            break
    return header_height

<<<<<<< HEAD
# flatten a multi dimensional list into a 1D list
# IE: [[[1, 2], 3], [4, 5]] -> [1, 2, 3, 4, 5]
=======
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
def flatten(tags):
    flattened_tags = []
    for sentence in tags:
        flattened_tags.extend(sentence)
    return flattened_tags

<<<<<<< HEAD
# extract the table title from the .json Adobe provides
=======
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
def extractTitle(path):
    global tagged_titles
    global titles
    global tags

    titles_list = []
    data = json.load(open(path, encoding='UTF-8'))
<<<<<<< HEAD
    # search through all the elements in the .json
    for i in range(len(data['elements'])):
        elem = data['elements'][i]
        elem_path = elem['Path']
        # find the elements that are tables
        if re.match('^//Document/(.*?)Table(\[[0-9]+\])?$', elem_path):
            title_elem = data['elements'][i - 1]
            if 'Text' in title_elem:
                # store the title
                title = title_elem['Text']
                # tag the title and store it into titles_list
=======
    for i in range(len(data['elements'])):
        elem = data['elements'][i]
        elem_path = elem['Path']
        if re.match('^//Document/(.*?)Table(\[[1-9]\])?$', elem_path):
            title_elem = data['elements'][i - 1]
            if 'Text' in title_elem:
                title = title_elem['Text']
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
                flattened_tags = flatten(ner_model.tag_doc(title))
                titles_list.append(flattened_tags)
            else:
                titles_list.append("")
    for full_title in titles_list:
        tagged_title = []
        title = ""
        tag = []
<<<<<<< HEAD
        # iterate through each title
        for word in full_title:
            # if the tag is not o(other), store the word in the title in tagged title
            if word[1] != 'O':
                tagged_title.append(word[0])
                tag.append(word[1])
            # store the title itself
            title += word[0] + " "
        # add the tagged title, title, and tags to separate lists
        tagged_titles.insert(0, tagged_title)
        titles.insert(0, title)
        tags.insert(0, tag)


# Extract data from xlsx files
=======
        for word in full_title:
            if word[1] != 'O':
                tagged_title.append(word[0])
                tag.append(word[1])
            title += word[0] + " "
        tagged_titles.append(tagged_title)
        titles.append(title)
        tags.append(tag)



# To open Workbook
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
def extractTable(path, subdir):
    global elems
    global cellCount
    global titles
    global tagged_titles
    global tags
<<<<<<< HEAD
    # get the title of the PDF
    path_list = subdir.split("\\")
    pdf_title = path_list[len(path_list)-2]

    # retrieve the pdf title, tag, and tagged title
=======

    pdf_title = subdir.split("\\")[8]

>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
    title = titles.pop()
    tag = tags.pop()
    tagged_title = tagged_titles.pop()

<<<<<<< HEAD
    # read the xlsx files using xlrd
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)

    # count the total # of cells in the table
    cellCount = [sheet.ncols] * sheet.nrows

    if len(cellCount) > 0:
        # check if the first row of the table is a single merged cell
        start = 0
        if len(sheet.merged_cells)>0:
            rlo, rhi, clo, chi =  sheet.merged_cells[0]
            # if it is, Adobe likely extracted the table title with the table
            if rhi == 1 and rlo == 0 and chi-clo == sheet.ncols:
                # correct table title
                title = unmergedValue(0, 0, sheet)
                start = 1


        # determine how many rows are headers
        header_height = detectHeaders(sheet, start)

        # extract the headers in the table and flatten them with | separating the headers
        headers = []
        for col in range(sheet.ncols):
            header = []
            for row in range(start, header_height):
                header.append(''.join(unmergedValue(row, col, sheet).replace('.', '').splitlines()))
            headers.append(' | '.join(header))

        # insert the rest of the data in the table
        for row in range(header_height, sheet.nrows):
            table = []
            # for each cell, create a key-value pair with the header above it and the value of the cell
            for col in range(sheet.ncols):
                d = {'name': headers[col], 'value': ''.join(unmergedValue(row, col, sheet).splitlines())}
                table.append(d)
            # add additional metadata to the row including the table title, tagged title, tags, and pdf title
            elems.append({'body': table, 'title': title, 'tagged_title': tagged_title, 'tags': tag, 'pdf_title': pdf_title})

# iterate through the folder with the extracted data from Adobe

def iterateDict():
    for subdir, dirs, files in os.walk(folderPath):
        # sort the xlsx files by their number so the table title extracted from the .json is correct
        for file in sorted(files, key=natural_keys):
            # if the file ends with xlsx, run extractTable
            if file.endswith('.xlsx'):
                extractTable(os.path.join(subdir, file), subdir)
            # if the file ends with .json, extract the titles
            if file.endswith('.json'):
                extractTitle(os.path.join(subdir, file))

# run the iterateDict which starts the process
iterateDict()

# inform user that the insertion is complete
print("Insertion complete")
# insert the data into MongoDB Atlas
db.ElsevierHEACreepPDFs.insert_many(elems)
=======
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)

    cellCount = [sheet.ncols] * sheet.nrows
    header_height = detectHeaders(sheet)

    headers = []
    for col in range(sheet.ncols):
        header = []
        for row in range(header_height):
            header.append(''.join(unmergedValue(row, col, sheet).replace('.', '').splitlines()))
        headers.append(' | '.join(header))

    for row in range(header_height, sheet.nrows):
        table = []
        for col in range(sheet.ncols):
            d = {'name': headers[col], 'value': ''.join(unmergedValue(row, col, sheet).splitlines())}
            table.append(d)
        elems.append({'body': table, 'title': title, 'tagged_title': tagged_title, 'tags': tag, 'pdf_title': pdf_title})


def iterateDict():
    for subdir, dirs, files in os.walk(folderPath):
        for file in sorted(files, key=natural_keys):
            if file.endswith('.xlsx'):
                print(str(file))
                extractTable(os.path.join(subdir, file), subdir)
            if file.endswith('.json'):
                extractTitle(os.path.join(subdir, file))


iterateDict()
print("Insertion complete")
db.data.insert_many(elems)
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
