# TableExtraction

ExtractFiles - Take the zip folders from Adobe's API containing the extracted PDF tables and metadata and unzip them. 

LBNLP - A test program for the NLP library

ProcTable - Extract the table data and metadata from the xlsx and .json files from Adobe's PDF extraction API and insert the extracted data into MongoDB Atlas for cloud acess

Table Counter - Script to count the current number of tables in a directory


## procTable
lists:
elems = []

cellCount = []

tagged_titles = []

titles = []

tags = []

extractTable function extract data from xlsx files
    pdf_title: same for files in the same folder, for example, ElsevierHEACreepPDFs.