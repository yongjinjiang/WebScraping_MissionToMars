from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
# from scrapy_mars import scrape
# import os

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