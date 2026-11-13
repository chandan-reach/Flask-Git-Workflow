
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("MongoDB connected successfully!")

    db = client["flask_database"]
    collection = db["submissions"]

except Exception as e:
    print("MongoDB connection failed!")
    print(e)
    client = None
    collection = None


# Home page and form submission
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            data = {
                "name": name,
                "email": email,
                "message": message
            }

            if collection is None:
                raise Exception("MongoDB is not connected")

            collection.insert_one(data)

            return redirect(url_for("success"))

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


# API route to read data.json
@app.route("/api")
def api():

    with open("data.json", "r") as file:
        data = json.load(file)

    return data


if __name__ == "__main__":
    app.run(debug=True)
