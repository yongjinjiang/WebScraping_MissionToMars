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


chrome_options = Options()
chrome_options.binary_location = GOOGLE_CHROME_BIN
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)


# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
executable_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}

# browser = Browser('chrome', **executable_path, headless=False)
# browser = Browser('django')
browser = Browser('chrome', **executable_path, headless=False)
url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[4]:


#len(soup)


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrapy_mars import scrape
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_db"


# In[ ]:
@app.route("/")
def index():
   # listings = mongo.db.Mars.find_one()
   return "hello"


if __name__ == "__main__":
    app.run(debug=True)




