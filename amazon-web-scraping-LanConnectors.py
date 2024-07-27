#!/usr/bin/env python
# coding: utf-8

# In[47]:


pip install bs4


# In[2]:


pip install requests


# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
import requests


# In[2]:


url="https://www.amazon.com/s?k=lan+connector&ref=nb_sb_noss"


# In[3]:


Headers=({'User-Agent':'https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes','Accept-Language':'en-US,en;q=0.5'})


# In[4]:


webpage=requests.get(url,headers=Headers)


# In[5]:


webpage


# In[6]:


webpage.content


# In[7]:


type(webpage.content)


# In[8]:


all_data=BeautifulSoup(webpage.content,'html.parser')


# In[9]:


all_data


# In[10]:


all_links=all_data.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})


# In[11]:


all_links


# In[12]:


new_link="https://amazon.com"+all_links[0].get('href')


# In[13]:


new_link


# In[14]:


new_webpage=requests.get(new_link,headers=Headers)


# In[15]:


new_webpage


# In[16]:


new_webcontent=BeautifulSoup(new_webpage.content,'html.parser')


# In[17]:


new_webcontent


# In[18]:


new_webcontent.find("span",attrs={"id":"productTitle"}).text.strip()


# In[19]:


new_webcontent.find("span",attrs={"class":"a-offscreen"}).text


# In[20]:


new_webcontent.find("span",attrs={"class":"a-icon-alt"}).text


# In[21]:


new_webcontent.find("a",attrs={"id":"bylineInfo"}).text[7:]


# In[22]:


new_webcontent.find("span",attrs={"class":"selection"}).text.strip()


# In[23]:


def get_title(wcontent):
  try:
    t=wcontent.find("span",attrs={"id":"productTitle"}).text.strip()
  except AttributeError:
    t=" "
  return t


# In[24]:


def get_price(wcontent):
  try:
    p=wcontent.find("span",attrs={"class":"a-offscreen"}).text.strip()
  except AttributeError:
    p=" "
  return p


# In[25]:


def get_rating(wcontent):
  try:
    r=wcontent.find("span",attrs={"class":"a-icon-alt"}).text
  except AttributeError:
    r=" "
  return r


# In[26]:


def get_brand(wcontent):
  try:
    b=wcontent.find("a",attrs={"id":"bylineInfo"}).text[7:]
  except AttributeError:
    b=" "
  return b


# In[27]:


def get_color(wcontent):
  try:
    b=wcontent.find("span",attrs={"class":"selection"}).text.strip()
  except AttributeError:
    b=" "
  return b


# In[28]:


d = {"title":[], "price":[], "rating":[], "brand":[]}


# In[29]:


for link in all_links:
    print("https://www.amazon.com" + str(link.get('href')))
    print("\n")


# In[30]:


for link in all_links:
  link="https://www.amazon.com"+link.get('href')
  page=requests.get(link,headers=Headers)
  wcontent=BeautifulSoup(page.content,'html.parser')
  d['title'].append(get_title(wcontent))
  d['price'].append(get_price(wcontent))
  d['rating'].append(get_rating(wcontent))
  d['brand'].append(get_brand(wcontent))


# In[31]:


import numpy as np
amazon_df = pd.DataFrame.from_dict(d)
amazon_df['title'].replace('', np.nan, inplace=True)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv("amazon_data.csv", header=True, index=False)


# In[32]:


data=amazon_df
data


# In[33]:


type(data)


# In[ ]:




