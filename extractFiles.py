<<<<<<< HEAD
# Extract the output files
=======
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
import zipfile
import os
import glob

<<<<<<< HEAD
path = r"C:\Users\Jason\OneDrive\Documents\pdfservices-java-sdk-samples-master\output\ElsevierSuperAlloyPDFs"

for arc_name in glob.iglob(os.path.join(path, "*.zip")):

=======
path = r"C:\Users\Jason\Documents\pdftools\adobe-dc-pdf-services-sdk-java-samples\output"

os.chdir(path)

for arc_name in glob.iglob(os.path.join(path, "*.zip")):
>>>>>>> bc13ca7a9209d1d0e2ebfd6aa7ef51e108b3f073
    arc_dir_name = os.path.splitext(os.path.basename(arc_name))[0]
    zf = zipfile.ZipFile(arc_name)
    zf.extractall(path=os.path.join(path, "ExtractedData", arc_dir_name))
    zf.close()