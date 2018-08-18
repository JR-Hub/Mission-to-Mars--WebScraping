# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
# from flask_pymongo import PyMongo
import pymongo
import sys
import scrape_mars

# create instance of Flask app
app = Flask(__name__)


# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)


db = client.mars_db
# collection = db.mars


@app.route("/")
def home():
   mars_info = db.mars_d.find_one()
   return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
   db.mars_d.drop()
   mars=scrape_mars.scrape()
   db.mars_d.insert_one(mars)
   # Redirect back to home page
   return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
   app.run(debug=True)