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
import tweepy 
import sys
#sys.path.append('/Users/jyj/Dropbox/A_A_Data_Analysis/Group_Projects')
# Import Twitter API Keys
# from config import consumer_key, consumer_secret, access_token, access_token_secret
# # Setup Tweepy API Authentication
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())



def scrape():

            chrome_options = Options()
            chrome_options.binary_location = GOOGLE_CHROME_BIN
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)


            #NASA Mars latest News: this code block will generate latest_news
            executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
            browser = Browser('chrome', **executable_path, headless=False)

            url0="https://mars.nasa.gov/news/"
            url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.select('.list_text')
            latest_title=results[0].select('.content_title a')[0].get_text()
            latest_text=results[0].select('.article_teaser_body')[0].get_text()
            latest_title
            latest_text
            latest_news={"title":latest_title,"text":latest_text}
           


            #JPL Mars Space Images - Featured Image: this code block will generate featured_image_url
            Mars_Space_Images="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars";
            browser.visit(Mars_Space_Images)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.select('div.carousel_items')
            # results[0].select('article')[0]["style"]
            RE=re.compile(r"'/.*.jpg'")
            featured_image_url='https://www.jpl.nasa.gov'+RE.findall(results[0].select('article')[0]["style"])[0].strip("'")
            featured_image_url
            browser.visit(featured_image_url)



            #Mars Weather: this code block will get latest mars_weather mars_weather from twitter
            #method 1: web scraping 
            weather_url='https://twitter.com/marswxreport?lang=en'
            response = requests.get(weather_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            mars_weather = soup.select("li.js-stream-item")[0].select("p.TweetTextSize")[0].text
            mars_weather
            # # method2: get results by twitter api:
            # public_tweets = api.user_timeline("@MarsWxReport")
            # public_tweets[0]['text']


            # In[195]:


            #Mars Facts: this code block will get some facts (written in facts_dict/facts_df/facts_html)
            #about MAR
            facts_url="https://space-facts.com/mars/"
            response = requests.get(facts_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # len(soup.select("table"))
            col1=[a.get_text() for a in soup.select("table")[0].select(".column-1")]
            col1=[a.rstrip('[:]') for a in col1]
            col2=[a.get_text() for a in soup.select("table")[0].select(".column-2")]
            col2=[a.rstrip('\n') for a in col2]
            facts_dict = dict(zip(col1,col2))
            facts_dict
            
            #######
            tables = pd.read_html(facts_url)
            facts_df=tables[0].rename(columns={0:" ",1:"Value"}).set_index(" ")
            facts_df
            facts_html= facts_df.to_html()
            facts_html


            # In[196]:


            #Mars Hemispheres: this block code generate titles and url's for hemisphere images for MAr
            #which are included in a list of dicts hemisphere_image_urls:
            Hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
            response = requests.get(Hemispheres_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title=[]
            img_url=[]
            for item in  soup.select('a.itemLink'):
                title.append(item.select('h3')[0].get_text())
                url_enhanced="https://astrogeology.usgs.gov"+item["href"]
                response1 = requests.get(url_enhanced)
                soup1 = BeautifulSoup(response1.text, 'html.parser')
                img_url.append("https://astrogeology.usgs.gov"+soup1.select('img.wide-image')[0]['src'])
                
            hemisphere_image_urls = [{'title':title[i],'img_url':img_url[i]} for i in range(len(title))]
            hemisphere_image_urls


            # In[210]:


            #Now we put all the data into Mongo:

            # Initialize PyMongo to work with MongoDBs
            # conn = 'mongodb://localhost:27017'
            # conn="mongodb://heroku_dxww20g1:2m85ei2jvb8o3u8j6r994d8rqh@ds263791.mlab.com:63791/heroku_dxww20g1"
            


            str0=os.environ.get("MONGODB_URI")
            # str0="mongodb://heroku_dxww20g1:2m85ei2jvb8o3u8j6r994d8rqh@ds263791.mlab.com:63791/heroku_dxww20g1"
            print("str0=",str0)
            str1=str0.split('/');str1.pop;Mars_db=str1[-1];
            print("str1=",str1)
            str0='/'.join(str1)
           

            conn=str0
            client = pymongo.MongoClient(conn)

            
            # Define database and collection
            # client.drop_database('Mars_db')
            # db = client.Mars_db

            client.drop_database(Mars_db)
            db = client[Mars_db]


            collection = db.Mars_hemisphere_image_urls
            collection.drop()
            collection.insert_many(hemisphere_image_urls)
            results=collection.find()
            results=[result for result in results]
            results

            collection = db.Mars_facts_dict
            collection.drop()
            collection.insert_one(facts_dict)
            results=collection.find()
            results[0]

            

            collection = db.Mars_weather
            collection.drop()
            collection.insert_one({"mars_weather":mars_weather})
            results=collection.find()
            results[0]

            collection = db.Mars_latest_news
            collection.drop()
            collection.insert_one(latest_news)
            results=collection.find()
            results[0]

            collection = db.Mars_featured_image_url
            collection.drop()
            collection.insert_one({"featured_image_url":featured_image_url})
            results=collection.find()
            results[0]
            client.close()

            return None

            # import scrapy

