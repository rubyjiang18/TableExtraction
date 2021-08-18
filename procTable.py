import json
import os
import re
import xlrd
import pprint

from pymongo import MongoClient
from lbnlp.models.load.matscholar_2020v1 import load

mergeCol = 0

loc = "fileoutpart0.xlsx"
folderPath = r'C:\Users\Jason\Documents\pdftools\adobe-dc-pdf-services-sdk-java-samples\output\ExtractedData'
cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
client = MongoClient(cluster)
db = client.data

ner_model = load("ner")

elems = []
cellCount = []
tagged_titles = []
titles = []
tags = []

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def display(cursor):
    for document in cursor:
        print()
        pprint(document)


def unmergedValue(rowx, colx, thesheet):
    for crange in thesheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return thesheet.cell_value(rlo, clo)
    return thesheet.cell_value(rowx, colx)


def detectHeaders(sheet):
    header_height = 0
    global cellCount
    for crange in sheet.merged_cells:
        rlo, rhi, clo, chi = crange
        for row in range(rlo, rhi):
            cellCount[row] -= chi - clo
    maxCol = max(cellCount)
    for i in range(len(cellCount)):
        if cellCount[i] == maxCol:
            header_height = i + 1
            break
    return header_height

def flatten(tags):
    flattened_tags = []
    for sentence in tags:
        flattened_tags.extend(sentence)
    return flattened_tags

def extractTitle(path):
    global tagged_titles
    global titles
    global tags

    titles_list = []
    data = json.load(open(path, encoding='UTF-8'))
    for i in range(len(data['elements'])):
        elem = data['elements'][i]
        elem_path = elem['Path']
        if re.match('^//Document/(.*?)Table(\[[1-9]\])?$', elem_path):
            title_elem = data['elements'][i - 1]
            if 'Text' in title_elem:
                title = title_elem['Text']
                flattened_tags = flatten(ner_model.tag_doc(title))
                titles_list.append(flattened_tags)
            else:
                titles_list.append("")
    for full_title in titles_list:
        tagged_title = []
        title = ""
        tag = []
        for word in full_title:
            if word[1] != 'O':
                tagged_title.append(word[0])
                tag.append(word[1])
            title += word[0] + " "
        tagged_titles.append(tagged_title)
        titles.append(title)
        tags.append(tag)



# To open Workbook
def extractTable(path, subdir):
    global elems
    global cellCount
    global titles
    global tagged_titles
    global tags

    pdf_title = subdir.split("\\")[8]

    title = titles.pop()
    tag = tags.pop()
    tagged_title = tagged_titles.pop()

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
