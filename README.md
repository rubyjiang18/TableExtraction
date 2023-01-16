# TableExtraction

ExtractFiles - Take the zip folders from Adobe's API containing the extracted PDF tables and metadata and unzip them. 

LBNLP - A test program for the NLP library

ProcTable - Extract the table data and metadata from the xlsx and .json files from Adobe's PDF extraction API and insert the extracted data into MongoDB Atlas for cloud acess

Table Counter - Script to count the current number of tables in a directory


# Ebvironment setup notes:
The LBNLP version on GitHub had some issues. The first of which was compatibility issues between the dependencies the library uses (I'm not sure if this is the issue you are running into). The second issue I ran into was a problem with Window's encoding, however, I'm not sure if you will run into this issue as you are on Mac.

When I installed LBNLP, I created a list of steps I took (Note this is all for Windows however all of the pip commands should work with Mac).

1. Download VC++ complier (just selecct the desktop build tool)
https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. Install lbnlp:
pip install git+https://github.com/lbnlp/lbnlp.git

2. install NER requirements (tensorflow 1.15.0 requires python 3.7)
pip install -r [your_path]\lbnlp\requirements-ner.txt

3. install numpy version 1.18.4
pip install numpy==1.18.4

4. download data for ChemDataExtractor
cde data download

5. show all installed package
pip list

6. Requirements for running the ner module on lbnlp
tensorflow==1.15.0
numpy==1.18.4
gensim==3.7.1
pymatgen==2019.9.8

7. modify file open, add utf-8 to file open call
[your_path]\Python\Python37\Lib\site-packages\lbnlp\ner\data_utils.py
line 191:  with open(filename, encoding='utf-8') as f:

This last step is to fix the encoding issue with Windows as it uses CP1252 encoding by default, however, Mac uses UTF-8 by default so this should not be an issue.

8. pip install protobuf==3.20.*


# procTable
lists:
elems = []
cellCount = []
titles = [], this is title of each table.

tagged_titles = [], this is the word in the tablt title this is being tagged. It should be renamed into tagged_word for better understanding. But we will keep it title so far to keep the MongoDB consistent.
tags = [], this is tag for the tagged_title.

Example word = ('crystallographic', 'B-PRO'), word[0] is tagged_title, word[1] is tag.