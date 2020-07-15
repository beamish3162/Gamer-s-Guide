import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone_project"
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_games")
def get_games():
    return render_template("index.html", 
                           games=mongo.db.games.find(), consoles=mongo.db.consoles.find())


@app.route("/list_games")
def list_games():
    return render_template("games-list.html", games=mongo.db.games.find())


@app.route("/game_page/<int:game_id>", methods=["GET"])
def game_page(game_id):
    the_game =  mongo.db.games.find_one({"_id": game_id})
    return render_template("game-page.html", games=mongo.db.games.find(), this_game=the_game)


@app.route("/add_game")
def add_game():
    return render_template("addgame.html", consoles=mongo.db.consoles.find(),
                           games=mongo.db.games.find())


@app.route("/insert_game", methods=['POST'])
def insert_game():
    col.insert_one
    return redirect(url_for('list_games'), consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find(), scores=mongo.db.score.find(),
                           games=mongo.db.games.find())
    

@app.route("/add_review")
def add_review():
    return render_template("addreview.html", consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find(), scores=mongo.db.score.find(),
                           games=mongo.db.games.find())



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
