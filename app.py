# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
import numpy as np
import re
import os
###twitter
import json


# In[2]:


## https://splinter.readthedocs.io/en/latest/drivers/chrome.html
#get_ipython().system('which chromedriver')
#

# In[3]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path, headless=False)
# browser = Browser('django')
browser = Browser('chrome', **executable_path, headless=False)
url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[4]:


len(soup)


# In[ ]:




