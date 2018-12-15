#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy
class TestSpider(scrapy.Spider):
    name = "test"

    start_urls = [
        "http://stackoverflow.com/questions/38233614/download-a-full-page-with-scrapy",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)


# In[ ]:




