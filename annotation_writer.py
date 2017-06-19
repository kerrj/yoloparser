import xml.etree.ElementTree as ET
import os
class BoundingBox():
    xmin,xmax,ymin,ymax=0,0,0,0
    name=''
    def __init__(self,name,xmin,ymin,xmax,ymax):
        self.name=name
        self.xmin=xmin
        self.ymin=ymin
        self.ymax=ymax
        self.xmax=xmax


def save_annotation(imgname,bboxes,savedir,imgwidth,imgheight):
    '''
    imgname=name of image file to save eg "0001.jpg"
    bboxes=list of bounding boxes in the image
    savedir=root dir to save annotation in
    '''   
    name=imgname.split('.')[0]
    extension='.'+imgname.split('.')[1]
    annotation=ET.Element('annotation')
    filename=ET.SubElement(annotation,'filename')
    filename.text=name+'.jpg'
    if savedir[-1]!='/':
        savedir+='/'    
    size=ET.SubElement(annotation,'size')
    width=ET.SubElement(size,'width')
    width.text=str(imgwidth)
    height=ET.SubElement(size,'height')
    height.text=str(imgheight)
    depth=ET.SubElement(size,'depth')
    depth.text='3'
    
    
    for bbox in bboxes:
        obj=ET.SubElement(annotation,'object')
        n=ET.SubElement(obj,'name')
        n.text=bbox.name
        bndbox=ET.SubElement(obj,'bndbox')
        xmin=ET.SubElement(bndbox,'xmin')
        xmin.text=str(bbox.xmin)
        ymin=ET.SubElement(bndbox,'ymin')
        ymin.text=str(bbox.ymin)
        xmax=ET.SubElement(bndbox,'xmax')
        xmax.text=str(bbox.xmax)
        ymax=ET.SubElement(bndbox,'ymax')
        ymax.text=str(bbox.ymax)     
        
        
    etree=ET.ElementTree(annotation)
    etree.write(savedir+name+'.xml')
    return

def load_annotation(imgname):
    name=imgname.split('.')[0]
    root=ET.parse('./static/annotations/'+name+'.xml')
    bounding_boxes=[]
    for obj in root.findall('object'):
        name=obj.find('name').text
        bndbox=obj.find('bndbox')
        xmin=int(float(bndbox.find('xmin').text))
        ymin=int(float(bndbox.find('ymin').text))
        xmax=int(float(bndbox.find('xmax').text))
        ymax=int(float(bndbox.find('ymax').text))
        bounding_boxes.append(BoundingBox(name,xmin,ymin,xmax,ymax))
    return bounding_boxes

if __name__=='__main__':
    print(load_annotation('20170618_113023.jpg'))