# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os

#Use only your files are in-order
def ImageConcat(path):
  FirstTime = True
  for filename in os.listdir(path):
      img = cv2.imread(os.path.join(path,filename))
      if FirstTime == True:
        Concat_img = img
        FirstTime = False
        pass
      if img is not None:
          Concat_img = np.concatenate((Concat_img, img),axis = 1)
  path = path+'output'+'.png'
  cv2.imwrite(path,Concat_img)