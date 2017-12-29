import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

mypath = "self/"   #路径  
outpath = "suotxt/"

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

##def convert_annotation(celltype, txt_id):
##    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
##    out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
##    tree=ET.parse(in_file)
##    root = tree.getroot()
##    size = root.find('size')
##    w = int(size.find('width').text)
##    h = int(size.find('height').text)
##
##    for obj in root.iter('object'):
##        difficult = obj.find('difficult').text
##        cls = obj.find('name').text
##        if cls not in classes or int(difficult) == 1:
##            continue
##        cls_id = classes.index(cls)
##        xmlbox = obj.find('bndbox')
##        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
##        bb = convert((w,h), b)
##        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

def convert_suo(size,pos):
    for i in range(len(pos)):
        pos[i] = float(pos[i])
    dw = 1./size[0]
    dh = 1./size[1]
    x = (pos[0] + pos[2])/2.0
    y = (pos[1] + pos[5])/2.0
    w = pos[2] - pos[0]
    h = pos[5] - pos[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    new_pos = str(x),str(y),str(w),str(h)
    return (list(new_pos))

##in_file = open("self/%s.txt"%(old_id),'r')
##out_file = open("self/%s.txt"%(old_id(5:)),'w')

def convert_type(old_type):
    num_lis = [0,11,3,11,1,1]     #总数27
    new_type = 0
    
    for i in range(int(old_type[0])):
        new_type += num_lis[i]
    if (old_type[1]==0):
        old_type[1]=1
    new_type += int(old_type[1])
    return (str(new_type))
    
def convert_suofile(path):
    list_file = open(path,"r")
    img_arr = list_file.readlines()
    
    cell_sum = img_arr[0]
    old_cell_type_arr = []
    cell_type_arr = []
    cell_pos_arr = []
    new_cell_info = []

    for i in range(len(img_arr)):
        if len(img_arr[i]) <=15:
            old_cell_type_arr.append(img_arr[i].strip("\n"))
        else:
            cell_pos_arr.append(img_arr[i])

    for i in range(len(old_cell_type_arr)-1):
        for j in range(int(old_cell_type_arr[i+1].strip().split()[2])):
            cell_type_arr.append(''.join(old_cell_type_arr[i+1].strip().split()[0:2]))
            
    for i in range(int(cell_sum)):
        pos_lis = cell_pos_arr[i].split()
        str1 = convert_type(cell_type_arr[i]) +" " + " ".join(convert_suo([800,600],pos_lis))
        new_cell_info.append(str1+"\n")
    list_file.close()
    return(new_cell_info)


old_filelist=[]
new_filelist=[]

for root, dirs, files in os.walk(mypath):   #遍历文件夹
    for name in files:
        if name[-4:] == ".txt":
            old_filelist.append(os.path.join(root,name))
            new_filelist.append(os.path.join(root,name[5:]))

for i in range(len(new_filelist)):       #写入文件
    os.system(new_filelist[i])
    out_file = open(new_filelist[i],"w")        
    out_file.write("".join(convert_suofile(old_filelist[i])))
    out_file.close()
    


