from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    print('in scrape')
    mars = mongo.db.mars
    print('connected to mars table')
    mars_info = scrape_mars.scrape()
    print('finished scrape')
    mars.update({}, mars_info, upsert=True)
    print('updated mongo')
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)