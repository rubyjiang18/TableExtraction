import tabulate
from pymongo import MongoClient
import pandas as pd
import csv

# cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

# Link to the MongoDB cluster
cluster = "mongodb://table_extraction:vlldc3JRnDG2DvW3@cluster0-shard-00-00.afvrd.mongodb.net:27017,cluster0-shard-00-01.afvrd.mongodb.net:27017,cluster0-shard-00-02.afvrd.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-12bs5c-shard-0&authSource=admin&retryWrites=true&w=majority"

client = MongoClient(cluster)

# Get the database
db = client.data

# Get all of the clusters
db_Test = db.data
db_Melt_Pool = db.Melt_Pool
db_Refractory_Alloys = db.Refractory_Alloys
db_Super_Alloys = db.Super_Alloys
db_Mechanical_Properties = db.Mechanical_Properties
db_HEA_Creep = db.ElsevierHEACreepPDFs
db_Super_Alloys_Creep = db.ElsevierSuperAlloyPDFs

# Add the clusters into a list
collection_list = {
    'All': [db_Test, db_Melt_Pool, db_Refractory_Alloys, db_Super_Alloys, db_Mechanical_Properties, db_HEA_Creep,
            db_Super_Alloys_Creep], 'Test': [db_Test], 'Mechanical Properties': [db_Mechanical_Properties],
    'Melt Pool': [db_Melt_Pool], 'Refractory Alloys': [db_Refractory_Alloys], 'Super Alloys': [db_Super_Alloys],
    'Hea Creep': [db_HEA_Creep], 'Super Alloys Creep': [db_Super_Alloys_Creep]}
value = ""
searchType = ""
df_dict = []
lastSearch = ""

doi_dict = {}
reader = csv.reader(open('doi.csv', 'r', encoding="utf8"))
for k, v in reader:
    doi_dict[k] = v

print(doi_dict)


# Bold text formatting
class font:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Merge title with tagged title
def merge(list1, list2):
    merged_list = ["(" + list1[i] + ", " + list2[i] + ")" for i in range(0, len(list1))]
    return merged_list


def mergeTables(df_dict):
    b = len(df_dict)
    cbdf_list = {}
    if len(df_dict) > 0:
        df = df_dict[0]
        df = df.reindex(sorted(df.columns), axis=1)
        # saving inside cbdf_list dictionary as lists
        names = list(df.columns)
        for j in range(len(names)):
            cbdf_list[names[j]] = df[names[j]].tolist()

        for i in range(b - 1):
            i = i + 1
            df = df_dict[i]
            df = df.reindex(sorted(df.columns), axis=1)
            names = list(df.columns)
            temp = {}
            for j in range(len(names)):
                new = True
                for k, v in cbdf_list.items():
                    if names[j].lower().strip() == k.lower().strip():
                        cbdf_list[k].extend(df[names[j]].tolist())
                        new = False
                if new:
                    temp[names[j]] = [None] * len(v)
                    temp[names[j]].extend(df[names[j]].tolist())
            cbdf_list.update(temp)
            lengths = [len(v) for v in cbdf_list.values()]
            max_L = max(lengths)
            for k, v in cbdf_list.items():
                if len(v) < max_L:
                    diff = max_L - len(v)
                    emp_L = [None] * diff
                    cbdf_list[k].extend(emp_L)
    return cbdf_list


# Print out the "cursor"
def display(cursor, type, search_elem):
    global value
    global searchType
    global df_dict
    search_elem = search_elem.lower()
    last_title = ""
    print("Searches found: " + str(len(list(cursor.clone()))))
    print("____________________________________________ \n \n ")
    output_list = []
    first = True
    rows = []
    header = []
    output_dict = {}
    id_list = []
    flagged = False
    # table_count = 0
    for document in cursor:
        flag = False
        if searchType == 'Off':
            if type == "name" or type == "value" or type == "both":
                for elem in document['body']:
                    if type == "name" or type == "value":
                        if search_elem in elem[type].lower().split(" "):
                            flag = True
                    else:
                        if search_elem in elem['name'].lower().split(" ") or search_elem in elem[
                            'value'].lower().split():
                            flag = True
            else:
                if search_elem in document[type].lower().split(" "):
                    flag = True
        else:
            flag = True
        if flag:
            output = {}
            # document_list[table_count].append(document)
            for elem in document['body']:
                output[elem['name']] = elem['value']
            if len(rows) == 1:
                output_dict['pdf_title'] = "PDF Title:" + " " + document['pdf_title']
                # print(font.BOLD + font.UNDERLINE + "PDF Title:" + font.END + " " + document['pdf_title'])
                output_dict['title'] = "Title:" + " " + document['title']
                # print(font.BOLD + font.UNDERLINE + "Title:" + font.END + " " + document['title'])
                tagged_title = merge(document['tagged_title'], document['tags'])
                output_dict['tagged_title'] = "Tagged Title: " + ", ".join(tagged_title)
                if document['pdf_title'] in doi_dict:
                    output_dict['doi'] = doi_dict[document['pdf_title']]
                else:
                    output_dict['doi'] = "none"

                # print(font.BOLD + font.UNDERLINE + "Tagged Title:" + font.END + " " + ", ".join(tagged_title))
                header_format = [elem for elem in output.keys()]
                header = list(output.keys())
                rows.append(list(output.values()))

                # id_list.append(document['_id'])

            if last_title != document['title'] and not first:
                table_dict = {}
                for i in range(len(header)):
                    col = []
                    for row in rows:
                        if len(row) > i:
                            col.append(row[i])
                        else:
                            col.append('')
                    table_dict[header[i]] = col
                df_dict.append(pd.DataFrame(table_dict))
                output_dict['table'] = tabulate.tabulate(rows, header_format)
                output_dict['id'] = id_list
                id_list = []
                flagged = False
                output_list.append(output_dict)
                output_dict = {}
                # str_output += "\n\n_______________________________________________________________________________________________\n\n"
                rows = []
            if not flagged:
                output_dict['flagged'] = document['Flag']
            id_list.append(document['_id'])
            rows.append(list(output.values()))
            last_title = document['title']
            first = False
    return output_list


# Search only in the header. Return cursor with elements containing the desired value in the header
def searchHeader(elem, db):
    cursor = db.find({
        'body': {'$elemMatch': {'name': {'$regex': elem}}}
    })
    return cursor


# Search only in the Value. Return cursor with elements containing the desired value in the table
def searchValue(elem, db):
    cursor = db.find({
        'body': {'$elemMatch': {'value': {'$regex': elem}}}
    })
    return cursor


# Search both the header and value. Return cursor with elements that contain the desired header or value in the table
def searchHeaderValue(elem, db):
    cursor = db.find({
        '$or': [
            {'body': {'$elemMatch': {'value': {'$regex': elem}}}},
            {'body': {'$elemMatch': {'name': {'$regex': elem}}}}
        ]
    })
    return cursor


# Same as above but with the PDF Title
def searchPDFTitle(elem, db):
    cursor = db.find({'pdf_title': {'$regex': elem}})
    return cursor


# Same as above but with the table title
def searchTitle(elem, db):
    cursor = db.find({'title': {'$regex': elem}})
    return cursor


# Same as above but with table title tags
def searchTags(elem, db):
    cursor = db.find({
        'tags': {'$elemMatch': {'$regex': elem}}
    })
    return cursor


running = True


def search(searchParam, searchType, searchDatabase, value):
    global lastSearch
    # Prompt user

    collections = collection_list[searchDatabase]
    for collection in collections:
        if searchParam == 'Table header':
            return display(searchHeader(value, collection), "name", value)
        elif searchParam == 'Value':
            return display(searchValue(value, collection), "value", value)
        elif searchParam == 'Header and Value':
            return display(searchHeaderValue(value, collection), "both", value)
        elif searchParam == 'PDF Title':
            return display(searchPDFTitle(value, collection), "pdf_title", value)
        elif searchParam == 'Table Title':
            return display(searchTitle(value, collection), "title", value)
        elif searchParam == 'Tagged Title':
            return display(searchTags(value, collection), "tags", value)
        else:
            print('Please input a number')
        lastSearch = value + searchParam + searchType + searchDatabase


def csvOutput():
    global df_dict
    global lastSearch
    cbdf_list = mergeTables(df_dict)
    cbdf = pd.DataFrame.from_dict(cbdf_list)
    i_csv = input("Would you like a csv with all the tables merged? (1) yes (2) no")
    if i_csv == '1':
        cbdf.to_csv(lastSearch + '.csv', index=False)
    df_dict = []


def update_flagged(id_list, flag):

    for m_db in collection_list['All']:
        for elem_id in id_list:
            m_db.update_one({
                '_id': elem_id
            }, {
                '$set': {
                    'Flag': flag
                }
            }, upsert=False)
