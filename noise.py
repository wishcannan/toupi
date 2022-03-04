import cv2
import numpy as np
# from numpy.core.fromnumeric import shape  
# import matplotlib.pyplot as plt
import os
#pip install Pillow
from PIL import Image
data = './static/img2/'

def lookimg(img,name):

    # cv2.imshow('64',img)
    # cv2.waitKey(0)
    # print(os.curdir)
    # cv2.imwrite(data+name,img)
    img = Image.fromarray(img)
    img.save(data+name)
    # plt.imshow(img)
    # plt.show()

def gaoshi(w,h,a):
    #a 强度
    # noise = np.random.rand(w,h)*a
    if not (w < 250 or h < 250):
        noise = np.random.normal(0.02,scale=a,size=(w,h))*255
        noise = cv2.GaussianBlur(noise,(3,3),1)
    elif not (w < 150 or h < 150):
        noise = np.random.normal(0,scale=a/3,size=(w,h))*255
        # noise = noise.astype('uint8')
        # noise = cv2.blur(noise,(3,3))
    # print(noise)
    else:
        noise = np.random.normal(0.05,scale=a/2,size=(w,h))*255
    return noise.astype('float64')

def lp(name):
    img = cv2.imread(data+name)
    mat = np.array(img,dtype='float64')
    w,h,channel = mat.shape
    # print(mat[:,:,0])
    for c in range(channel):
        noise = gaoshi(w,h,0.2)
        # print(mat[:,:,c])
        mat[:,:,c] += noise
        # np.where(mat[::c]<0, 0, mat[::c])
    mat = np.clip(mat,0,255).astype('uint8')
    lookimg(mat,name)
    # print(w,h,channel)

def lp2(file,name):#这个直接读文件 作为我们项目的功能 对外开放
    # print('图片进来了',file.filename)
    img = Image.open(file)
    # img = cv2.imread(file)
    mat = np.array(img,dtype='float64')
    w,h,channel = mat.shape
    # print(mat[:,:,0])
    for c in range(channel):
        noise = gaoshi(w,h,0.2)
        # print(mat[:,:,c])
        mat[:,:,c] += noise
        # np.where(mat[::c]<0, 0, mat[::c])
    mat = np.clip(mat,0,255).astype('uint8')
    lookimg(mat,name)
# lookimg('88334825.jpg')
# lp('88904389.jpg')
# a = './image/'
# i = os.listdir(a)
# for j in i:
#     lp(j)
# # print(i)