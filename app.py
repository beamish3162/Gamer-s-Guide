import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'milestone_project'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_games")
def get_games():
    return render_template("index.html", 
                           games=mongo.db.games.find(), consoles=mongo.db.consoles.find())


@app.route("/add_review")
def add_review():
    return render_template("addreview.html",  consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find(), scores=mongo.db.score.find())


@app.route('/insert_game', methods=['POST'])
def insert_game():
    games = mongo.db.games
    games.insert_one(request.form.to_dict())
    return redirect(url_for("get_games"))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
