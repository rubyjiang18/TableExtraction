import zipfile
import os
import glob

path = r"C:\Users\Jason\Documents\pdftools\adobe-dc-pdf-services-sdk-java-samples\output"

os.chdir(path)

for arc_name in glob.iglob(os.path.join(path, "*.zip")):
    arc_dir_name = os.path.splitext(os.path.basename(arc_name))[0]
    zf = zipfile.ZipFile(arc_name)
    zf.extractall(path=os.path.join(path, "ExtractedData", arc_dir_name))
    zf.close()