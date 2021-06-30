from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars as sm

app=Flask(__name__)
mongo=PyMongo(app,uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_scrape = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_scrape)

@app.route("/scrape")
def scrape():
    scrape_data=sm.scrape()
    mongo.db.mars_data.update_many({},{'$set':scrape_data},True)
    return redirect("/",code=302)

if __name__ == "__main__":
    app.run(debug=True)
