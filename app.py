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


@app.route("/game_page/<game_id>", methods=["GET"])
def game_page(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("game-page.html", game=the_game)


@app.route("/add_game")
def add_game():
    return render_template("addgame.html", consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find(), games=mongo.db.games.find())


@app.route("/insert_game", methods=["POST"])
def insert_game():
    games = mongo.db.games

    name = request.form['name']
    console_type = request.form['console_type']
    genre_type = request.form['genre_type']
    image = request.form['image']
    reviewer = request.form['reviewer']
    rating = request.form['rating']
    comments = request.form['comments']

    game_form = {
        'name': name,
        'console_type': console_type,
        'genre_type': genre_type,
        'image': image,
        'review': [{
            'reviewer': reviewer,
            'rating': rating,
            'comments': comments
        }]

    }
    games.insert_one(game_form)
    return redirect(url_for("list_games"))


@app.route("/add_review/<game_id>", methods=["GET"])
def add_review(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("addreview.html", game=the_game)


@app.route("/insert_review/<game_id>", methods=["POST"])
def insert_review(game_id):
    game = mongo.db.games
    reviewer = request.form['reviewer']
    rating = request.form['rating']
    comments = request.form['comments']

    game.update(
        {'_id': ObjectId(game_id)},
        {"$push": {"review":{
            "reviewer": reviewer,
            "rating": rating,
            "comments": comments
        }}}
    )
    return redirect(url_for("list_games"))


@app.route("/edit_game/<game_id>", methods=["GET"])
def edit_game(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("editgame.html", game=the_game, consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find())


@app.route("/update_game/<game_id>", methods=["POST"])
def update_game(game_id):
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    name = request.form['name']
    console_type = request.form['console_type']
    genre_type = request.form['genre_type']
    image = request.form['image']

    game.update(
        {"$set": {
            'name': name,
            'console_type': console_type,
            'genre_type': genre_type,
            'image': image
            }}
    )

    return redirect(url_for("list_games"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
