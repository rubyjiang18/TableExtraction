import os

folderPath = r'C:\Users\Jason\OneDrive\Documents\pdfservices-java-sdk-samples-master\output'

count = 0;

for subdir, dirs, files in os.walk(folderPath):
    for file in sorted(files):
        if file.endswith('.xlsx'):
            count += 1
print(count)