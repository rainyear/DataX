
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


# In[3]:


def fetch(url):
    cookie_str = 'login_sid_t=3eb7fb23c6eed8044f13fd595a5d3052; YF-V5-G0=73b58b9e32dedf309da5103c77c3af4f; _s_tentry=-; Apache=4142553613963.9087.1499961160557; SINAGLOBAL=4142553613963.9087.1499961160557; ULV=1499961160582:1:1:1:4142553613963.9087.1499961160557:; YF-Ugrow-G0=56862bac2f6bf97368b95873bc687eef; YF-Page-G0=46f5b98560a83dd9bfdd28c040a3673e; UM_distinctid=15d74bd136e502-0e2e5ae2aa2bad-30677808-1fa400-15d74bd136f519; httpsupgrade_ab=SSL; cross_origin_proto=SSL; SSOLoginState=1507816236; un=aplysia@126.com; wvr=6; UOR=,www.weibo.com,115.159.93.137:3000; SCF=AlX5LykRtR8Sq67oyApG_UOy9JNQwAjLBp0ooZ1WtskOrIoDvFJYjH0ZF9acKgsciLFvKOOr7f-6v5nGcgPvSGo.; SUB=_2A2505mckDeThGedJ7lIZ9SjEyjyIHXVXkt_srDV8PUNbmtBeLUrzkW8pU5g0bv8SHR-dnokYiyw5sspvTw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W54gQSJ.aHiu9XoHhdUlQUd5JpX5KMhUgL.Fo2NSK5RSKqReK52dJLoI7UyMsp4McLy; SUHB=0pHglsAtgYuqSB; ALF=1539525363'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Referer':'http://photo.weibo.com/tags/best/tag/%E4%BA%BA%E5%83%8F?prel=p3_1'
    }
    cookies = mk_cookie(cookie_str)
    res = req.get(url, headers = headers, cookies=cookies)
    return res

import re


client.dhub.authenticate("data", "data")
WB = client['dhub']['wb_user_copy']


# In[10]:


API_PHOTO = 'https://weibo.com/p/{}/photos'
rePhoto = re.compile(r'"photo_pict" src="(.*?)"')


# In[14]:


user = WB.find_one({"is_processed": False})
while user:
    if user.get("refer") is None:
        url = API_PHOTO.format(user['uid'])
    else:
        url = API_PHOTO.format("{}{}".format(user['refer'][:-4], user['uid']))
    print(url)
    res = fetch(url)
    html = res.text.replace("\\", "")
    photos = rePhoto.findall(html)
    WB.update_one({"uid": user['uid']}, {'$set': {"is_processed": True, "photos": photos}})
    user = WB.find_one({"is_processed": False})