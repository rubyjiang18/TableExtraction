import tabulate
from pymongo import MongoClient

cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
client = MongoClient(cluster)
db = client.data

class font:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def merge(list1, list2):
    merged_list = ["("+list1[i]+", "+list2[i]+")" for i in range(0, len(list1))]
    return merged_list

def display(cursor):
    print("Searches found: "+ str(cursor.count()))
    print("____________________________________________ \n \n ")
    for document in cursor:
        print(font.BOLD + font.UNDERLINE + "PDF Title:" + font.END + " " + document['pdf_title'])
        print(font.BOLD + font.UNDERLINE + "Title:" + font.END + " " + document['title'])
        tagged_title = merge(document['tagged_title'], document['tags'])
        print(font.BOLD + font.UNDERLINE + "Tagged Title:" + font.END + " " + ", ".join(tagged_title))
        output = {}
        for elem in document['body']:
            output[elem['name']] = elem['value']

        rows = [output.values()]
        header = [font.BOLD+ elem + font.END for elem in output.keys()]
        print(tabulate.tabulate(rows, header))
        print("\n\n_______________________________________________________________________________________________\n\n")

def searchHeader(elem):
    cursor = db.data.find({
        'body': {'$elemMatch': {'name': {'$regex': elem}}}
    })
    return cursor
def searchValue(elem):
    cursor = db.data.find({
        'body': {'$elemMatch': {'value': {'$regex': elem}}}
    })
    return cursor

def search(elem):
    cursor = db.data.find({
        '$or':[
            {'body': {'$elemMatch': {'value': {'$regex': elem}}}},
            {'body': {'$elemMatch': {'name': {'$regex': elem}}}}
        ]
    })
    return cursor

def searchPDFTitle(elem):
    cursor = db.data.find({'pdf_title': {'$regex': elem}})
    return cursor

def searchTitle(elem):
    cursor = db.data.find({'title': {'$regex': elem}})
    return cursor

def searchTags(elem):
    cursor = db.data.find({
        'tags': {'$elemMatch': {'$regex': elem}}
    })
    return cursor


running = True
while running:
    val = input("How would you like to search? (1)Table header, (2)Value, (3)Header and Value, (4)Pdf title, (5)Table title, or (6)Title tags: ")
    elem = input("What would you like to search for: ")
    if val == '1':
        display(searchHeader(elem))
    elif val == '2':
        display(searchValue(elem))
    elif val == '3':
        display(search(elem))
    elif val == '4':
        display(searchPDFTitle(elem))
    elif val == '5':
        display(searchTitle(elem))
    elif val == '6':
        display(searchTags(elem))
    else:
        print('Please input a number')


