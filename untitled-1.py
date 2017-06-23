import os 

for root,dirs,files in os.walk('./static/annotations'):
    files.pop(0)    
    for file in files:
        original=file
        file=file.replace(' ','')
        file=file.replace('_','')
        file=file.replace('-','')
        if original!=file:
            print(original,'-->',file)            
            os.rename('./static/annotations/'+original,'./static/annotations/'+file)