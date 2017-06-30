from flask import Flask,render_template,request,send_from_directory
import annotation_writer
import os
import random
import json
import requests
app=Flask(__name__)


@app.route('/')
def home():
    return render_template('homev2.html')

#@app.route('/review')
#def review():
    #return render_template('review.html')
    
@app.route('/saveresults',methods=['POST'])
def save():
    data=request.form
    numboxes=int(data['length'])
    imgname=data['imgname']
    owner=data['repoowner']
    rname=data['reponame']
    bboxes=[]
    for n in range(numboxes):
        xmin=data['boxes['+str(n)+'][xmin]']
        xmax=data['boxes['+str(n)+'][xmax]']
        ymin=data['boxes['+str(n)+'][ymin]']
        ymax=data['boxes['+str(n)+'][ymax]']
        name=data['boxes['+str(n)+'][name]']
        bboxes.append(annotation_writer.BoundingBox(name,xmin,ymin,xmax,ymax))
    annotation_writer.save_annotation(imgname,bboxes,'./static/annotations/'+owner+'/'+rname,data['width'],data['height'])
    return 'complete'

@app.route('/oops',methods=['POST'])
def oops():
    data=request.form
    image=data['image']
    owner=data['repoowner']
    name=data['reponame']
    os.remove('./static/annotations/'+owner+'/'+name+'/'+image.split('.')[0]+'.xml')
    return 'success'


#@app.route('/getnumannotations')
#def get_num_annotations():
    #for root,dirs,annotations in os.walk('./static/annotations'):
        #return str(len(annotations))
    
#@app.route('/remaining')
#def get_remaining():
    #for root,dirs,annotations in os.walk('./static/annotations'):
        #num_a=len(annotations)
    #for root,dirs,images in os.walk('./static/images'):
        #num_i=len(images)   
    #return str(num_i-num_a)

#@app.route('/getannotation',methods=['POST'])
#def get_annotation():
    #data=request.form
    #index=int(data['index'])
    #for root,dirs,files in os.walk('./static/annotations'):
        #annotations=files
    ##searching=True
    ##while searching:
        ##annotation=annotations[index]
        ##image=annotation.split('.')[0]+'.jpg'
        ##bboxes=annotation_writer.load_annotation(annotation)
        ##for box in bboxes:
            ##if box.name=='ball':
                ##searching=False
                ##break
        ##index+=1
        ##print(index)
    #annotation=annotations[index]
    #image=annotation.split('.')[0]+'.jpg'
    #bboxes=annotation_writer.load_annotation(annotation)    
    #boxesjson=''
    #for box in bboxes:
        #boxesjson+=box.to_json()+','
    #if boxesjson[-1]==',':
        #boxesjson=boxesjson[:-1]
    #boxesjson='['+boxesjson+']'
    #output=json.dumps({'annotation':annotation,'image':image,'bboxes':boxesjson})
    #return output
    

@app.route('/register',methods=['POST'])
def register_repo():
    data=request.form
    owner=data['repoowner']
    if owner.count('/')>0:
        return 'failed'
    name=data['reponame']
    if name.count('/')>0:
        return 'failed'
    
    try:
        os.mkdir('./static/annotations/'+owner)
    except OSError:
        pass
    try:
        os.mkdir('./static/annotations/'+owner+'/'+name)
    except:
        pass
        pass
    
    return ''

@app.route('/download/<path:owner>/<path:name>',methods=['GET','POST'])
def download(owner,name):
    import zipfile
    annotation_dir='./static/annotations/'+owner+'/'+name+'/'
    z=zipfile.ZipFile(annotation_dir+'annotations.zip',mode='w')
    for root,dirs,annotations in os.walk(annotation_dir):
        for annotation in annotations:
            if annotation!='annotations.zip' and annotation!='.DS_Store':
                z.write(annotation_dir+annotation)
    z.close()
    return send_from_directory(directory=annotation_dir,filename='annotations.zip')

@app.route('/getimage',methods=['POST'])
def load_image():
    data=request.form
    owner=data['repoowner']
    name=data['reponame']
    
    annotations=[]
    for root,dirs,files in os.walk('./static/annotations/'+owner+'/'+name):
        annotations=files
    
    succeeded,images=get_images_from_github(owner,name)
    random.shuffle(images)
    if succeeded:
        for image in images:
            name=image.split('.')[0]
            if annotations.count(name+'.xml')==0:
                return image
    return ''

def get_images_from_github(owner,name):
    '''
    returns [boolean succeeded, list of names]
    '''
    r=requests.get('https://api.github.com/repos/'+owner+'/'+name+'/contents')
    if(r.status_code!=200):
        return False,[]
    j=json.loads(r.text)
    names=[]
    for entry in j:
        names.append(entry.get('name'))
    return True, names