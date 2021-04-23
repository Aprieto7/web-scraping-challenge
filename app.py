from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # # Find one record of data from the mongo database
    return_data= mongo.db.return_data() 

    # # Return template and data
    return render_template("index.html", data=return_data)
    


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    return_data = mongo.db.return_data
    mars_data = scrape.scrape_info()
    
    # use mongo update to upsert data
    return_data.update({}, return_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
