
# coding: utf-8

# In[1]:


import requests as req

from pymongo import MongoClient
client = MongoClient()


# In[2]:


def mk_cookie(cstr):
    c = {}
    for i in cstr.split("; "):
        k, v = i.split("=")
        c[k] = v
    return c


# In[9]:


def fetch(url):
    cookie_str = 'login_sid_t=3eb7fb23c6eed8044f13fd595a5d3052; YF-V5-G0=73b58b9e32dedf309da5103c77c3af4f; _s_tentry=-; Apache=4142553613963.9087.1499961160557; SINAGLOBAL=4142553613963.9087.1499961160557; ULV=1499961160582:1:1:1:4142553613963.9087.1499961160557:; YF-Ugrow-G0=56862bac2f6bf97368b95873bc687eef; YF-Page-G0=46f5b98560a83dd9bfdd28c040a3673e; UM_distinctid=15d74bd136e502-0e2e5ae2aa2bad-30677808-1fa400-15d74bd136f519; httpsupgrade_ab=SSL; cross_origin_proto=SSL; SSOLoginState=1507816236; un=aplysia@126.com; UOR=,www.weibo.com,cn.bing.com; wvr=6; SCF=AlX5LykRtR8Sq67oyApG_UOy9JNQwAjLBp0ooZ1WtskOTGV3XkWYHYuOiLiaopomH4lUdrIkbE2h_SLg61c_dCE.; SUB=_2A2505LWRDeThGedJ7lIZ9SjEyjyIHXVXk6BZrDV8PUJbmtBeLRjgkW-eriQSdJvGvy7V5XLxAGFJYnB0Vg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W54gQSJ.aHiu9XoHhdUlQUd5JpX5K-hUgL.Fo2NSK5RSKqReK52dJLoIEBLxK-L1KeL1hnLxK-L1KeL1hnLxKML12qL1h5LxK-LB.qL1Kzt; SUHB=0xnTF8zXJpGQAx; ALF=1539438908; wb_cusLike_1750856810=N'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Referer':'http://photo.weibo.com/tags/best/tag/%E4%BA%BA%E5%83%8F?prel=p3_1'
    }
    cookies = mk_cookie(cookie_str)
    res = req.get(url, headers = headers, cookies=cookies)
    return res


# API_WITH_RID = "http://photo.weibo.com/tags/get_photos_by_tag_name?tag=%E4%BA%BA%E5%83%8F&count=20&page={page}&type=best&rid={rid}&__rnd={ts}"
# API = "http://photo.weibo.com/tags/get_photos_by_tag_name?tag=%E4%BA%BA%E5%83%8F&count=20&page={page}&type=best&__rnd={ts}"

# import time
import re

# def ts():
#     return int(time.time()*1000)

# In[82]:


client.dhub.authenticate("data", "data")
WB = client['dhub']['wb_user']


# In[123]:


reFan = re.compile(r'info_name W_fb W_f14([\s\S]*?)div>')
reUser = re.compile(r'id=(?P<uid>\d+)&refer_flag=(?P<refer>\d+)[\s\S]*?>(?P<nick>[\s\S]*?)<\/a>[\s\S]*?<i class="W_icon icon_(?P<sex>\w+)">')


# In[124]:


API_FOL = "https://weibo.com/p/{uid}/follow?relate=fans"


# In[125]:


MY_UID = "1005051750856810"


# In[126]:


res = fetch(API_FOL.format(uid = MY_UID))


# In[132]:


def process_fans(uid):
    url = API_FOL.format(uid = uid)
    print(url)
    res = fetch(url)
    html = res.text
    users = []

    for fan in reFan.findall(html):
        raw = fan.replace("\\", "")
        m = reUser.search(raw)
        if m:
            user = m.groupdict()
            user['is_processed'] = False
            users.append(user)
    return users


# In[133]:


users = process_fans("1005056092524936")
users = process_fans(MY_UID)


# In[135]:


WB.delete_many({})
WB.insert_one({"uid": MY_UID, "is_processed": False})


# In[136]:


i = 0
while True:
    u = WB.find_one({"is_processed": False})
    if not u or i > 10000:
        break
    
    ref = u.get("refer")
    if ref:
        uid = "{}{}".format(ref[:-4], u['uid'])
    else:
        uid = u['uid']
    users = process_fans(uid)
    for user in users:
        ex = WB.find_one({"uid": user['uid']})
        if not ex:
            print("User: {}".format(user['nick']))
            WB.insert_one(user)
    WB.update_one({"uid": u['uid']}, {"$set": {"is_processed": True}})
    i += 1


# rid = None
# for page in range(1, 500):
#     try:
#         if page == 1:
#             url = API.format(page = page, ts = ts())
#         else:
#             url = API_WITH_RID.format(page = page, rid = rid, ts = ts())
#         
#         print(url)
#         res = fetch(url)
#         if res.status_code == 200:
#             js = res.json()
#             rid = js['data']['rid']
#             photos = js['data']['photos']
#             WB.insert_many(photos)
#     except Exception as e:
#         print(e)
#         print("Failed at {}".format(url))

# In[ ]:




