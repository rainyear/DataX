
# coding: utf-8

# In[1]:


import cv2
import numpy  as np
import matplotlib.pyplot as plt


# In[2]:


# get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


face_cascade = cv2.CascadeClassifier('/home/ubuntu/.miniconda3/pkgs/opencv-3.1.0-np112py36_1/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')


# In[4]:


img = '/data/c10/data_x_warehouse/photos/1033028811-3d92c4cbly1fkbq6i8hwwj20hs0qon37.jpg'


# In[5]:


# img = cv2.imread(img)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
def det_faces(img):
    try:
        g = cv2.cvtColor(cv2.imread(img), cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(g, 1.1, 5)
        return len(faces)
    except:
        print("Failed")
        return 0


# In[6]:


det_faces(img)


# In[ ]:


from db import WB, WB_DL


# In[8]:


import os


# In[9]:


def img_name(uid, src):
    image_hash = src.split("?")[0].split("/")[-1]
    return "/data/c10/data_x_warehouse/photos/{}-{}".format(uid, image_hash)


# user = WB.find_one({"is_processed": False})
# while user:
#     dld = []
#     photos = user.get("photos")
#     for src in photos:
#         img = img_name(user['uid'], src)
#         if os.path.isfile(img):
#             dld.append({
#                 'uid': user.get("uid"),
#                 'sex': user.get("sex"),
#                 'img': img,
#                 'faces': 0,
#                 'is_processed': False
#             })
#     if len(dld):
#         WB_DL.insert_many(dld)
#     WB.update_one({'uid': user['uid']}, {'$set': {'is_processed': True}})
#     user = WB.find_one({"is_processed": False})
#     

# In[ ]:


user = WB_DL.find_one({"is_processed": False})
while user:
    faces = det_faces(user['img'])
    print("{} Faces {}".format(faces, user['img']))
    
    WB_DL.update_one({'_id': user['_id']}, {'$set': {'is_processed': True, 'faces': faces}})
    user = WB_DL.find_one({"is_processed": False})


# In[ ]:




