from flask import Flask,render_template,request
import annotation_writer
import os
import random
app=Flask(__name__)


@app.route('/')
def hi():
    return render_template('home.html')

@app.route('/saveresults',methods=['POST'])
def save():
    data=request.form
    numboxes=int(data['length'])
    imgname=data['imgname']
    bboxes=[]
    for n in range(numboxes):
        xmin=data['boxes['+str(n)+'][xmin]']
        xmax=data['boxes['+str(n)+'][xmax]']
        ymin=data['boxes['+str(n)+'][ymin]']
        ymax=data['boxes['+str(n)+'][ymax]']
        name=data['boxes['+str(n)+'][name]']
        bboxes.append(annotation_writer.BoundingBox(name,xmin,ymin,xmax,ymax))
    annotation_writer.save_annotation(imgname,bboxes,'./static/annotations',data['width'],data['height'])
    return 'complete'

@app.route('/getimage',methods=['GET'])
def load_image():
    annotations=[]
    for root,dirs,files in os.walk('./static/annotations'):
        annotations=files
    
    for root,dirs,images in os.walk('./static/images'):
        random.shuffle(images)
        for image in images:
            name=image.split('.')[0]
            if annotations.count(name+'.xml')==0:
                return image
    return ''   