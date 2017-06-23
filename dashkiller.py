import os 
import xml.etree.ElementTree as ET

for root,dirs,files in os.walk('./static/images'):
    for file in files:
        original=file
        file=file.replace('-','')
        if original!=file:
            print(original,'-->',file)            
            os.rename('./static/images/'+original,'./static/images/'+file)
for root,dirs,files in os.walk('./static/annotations'):
    for file in files:
        original=file
        file=file.replace('-','')
        if original!=file:
            print(original,'-->',file)            
            os.rename('./static/annotations/'+original,'./static/annotations/'+file)
            
for root,dirs,files in os.walk('./static/annotations'):
    files.pop(0)
    for file in files:
        print('Renaming xml name for',file)
        xmlroot=ET.parse('./static/annotations/'+file)
        filename=xmlroot.find('filename')
        name=filename.text
        name=name.replace('-','')
        filename.text=name
        xmlroot.write('./static/annotations/'+file)