import tabulate
from pymongo import MongoClient
import pandas as pd

#cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

# Link to the MongoDB cluster
cluster = "mongodb+srv://table_extraction:vlldc3JRnDG2DvW3@cluster0.afvrd.mongodb.net/?retryWrites=true&w=majority"

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
collection_list = {'1': [db_Test, db_Melt_Pool, db_Refractory_Alloys, db_Super_Alloys, db_Mechanical_Properties, db_HEA_Creep, db_Super_Alloys_Creep], '2': [db_Test], '3': [db_Mechanical_Properties],
                   '4': [db_Melt_Pool], '5': [db_Refractory_Alloys], '6': [db_Super_Alloys], '7': [db_HEA_Creep], '8': [db_Super_Alloys_Creep]}
value = ""
searchType = ""
df_dict = []


# Bold text formatting
class font:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Merge title with tagged title
def merge(list1, list2):
    merged_list = ["("+list1[i]+", "+list2[i]+")" for i in range(0, len(list1))]
    return merged_list

def mergeTables(df_dict):
    b = len(df_dict)
    cbdf_list = {}
    if len(df_dict) >0:
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
    first = True
    rows = []
    header = []
    for document in cursor:
        flag = False
        if(searchType == "1"):
            if type == "name" or type == "value" or type == "both":
                for elem in document['body']:
                    if type == "name" or type == "value":
                        if search_elem in elem[type].lower().split(" "):
                            flag = True
                    else:
                        if search_elem in elem['name'].lower().split(" ") or search_elem in elem['value'].lower().split():
                            flag = True
            else:
                if search_elem in document[type].lower().split(" "):
                    flag = True
        else:
            flag = True
        if flag:
            output = {}
            for elem in document['body']:
                output[elem['name']] = elem['value']
            if len(rows) == 1:
                print(font.BOLD + font.UNDERLINE + "PDF Title:" + font.END + " " + document['pdf_title'])
                print(font.BOLD + font.UNDERLINE + "Title:" + font.END + " " + document['title'])
                tagged_title = merge(document['tagged_title'], document['tags'])
                print(font.BOLD + font.UNDERLINE + "Tagged Title:" + font.END + " " + ", ".join(tagged_title))
                header_format = [font.BOLD + elem + font.END for elem in output.keys()]
                header = list(output.keys())

                rows.append(list(output.values()))
            if last_title != document['title'] and not first:
                output_dict = {}
                for i in range(len(header)):
                    col = []
                    for row in rows:
                        if len(row) > i:
                            col.append(row[i])
                        else:
                            col.append('')
                    output_dict[header[i]] = col
                df_dict.append(pd.DataFrame(output_dict))
                print(tabulate.tabulate(rows, header_format))
                print("\n\n_______________________________________________________________________________________________\n\n")
                rows = []
            rows.append(list(output.values()))
            last_title = document['title']
            first = False



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
def search(elem, db):
    cursor = db.find({
        '$or':[
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
while running:
    # Prompt user
    value = input("How would you like to search? (1)Table header, (2)Value, (3)Header and Value, (4)Pdf title, (5)Table title, or (6)Title tags: ")
    searchType = input("Would you like to search for (1)individual words or (2)parts of words?")
    searchDatabase = input("Would you like to search in (1) All databases (2) Test Database (3) Mechanical Properties (4) Melt Pool (5) Refractory Alloys (6) Super_Alloys (7) HEA Creep (8) Supper Alloys Creep")
    elem = input("What would you like to search for: ")

    collections = collection_list[searchDatabase]
    for collection in collections:
        if value == '1':
            display(searchHeader(elem, collection), "name", elem)
        elif value == '2':
            display(searchValue(elem, collection), "value", elem)
        elif value == '3':
            display(search(elem, collection), "both", elem)
        elif value == '4':
            display(searchPDFTitle(elem, collection), "pdf_title", elem)
        elif value == '5':
            display(searchTitle(elem, collection), "title", elem)
        elif value == '6':
            display(searchTags(elem, collection), "tags", elem)
        else:
            print('Please input a number')
    cbdf_list = mergeTables(df_dict)
    cbdf = pd.DataFrame.from_dict(cbdf_list)
    i_csv = input("Would you like a csv with all the tables merged? (1) yes (2) no")
    if i_csv == '1':
        cbdf.to_csv(elem+value+searchType+searchDatabase + '.csv', index=False)
    df_dict = []
    print("\n\n\n\n\n_______________________________________________________________________________________________\n\n")


