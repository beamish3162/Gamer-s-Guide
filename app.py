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
                           games=mongo.db.games.find(),
                           consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find())


@app.route("/list_games")
def list_games():
    games = mongo.db.games.find().sort('name')
    return render_template("games-list.html", games=games)


@app.route("/game_page/<game_id>", methods=["GET"])
def game_page(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    print(the_game)
    return render_template("game-page.html", game=the_game)


@app.route("/add_game")
def add_game():
    return render_template("addgame.html", consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find(),
                           games=mongo.db.games.find())


@app.route("/insert_game", methods=["POST", "GET"])
def insert_game():
    games = mongo.db.games
    name = request.form['name']
    PS4 = request.form["console_type_one"]
    XboxOne = request.form["console_type_two"]
    PC = request.form["console_type_three"]
    Nintendo_Switch = request.form["console_type_four"]
    genre_type = request.form['genre_type']
    image = request.form['image']
    reviewer = request.form['reviewer']
    rating = request.form['rating']
    comments = request.form['comments']

    game_form = {
        'name': name,
        'console_type': [{
            'one': PS4,
            'two': XboxOne,
            'three': PC,
            'four': Nintendo_Switch
        }],
        'genre_type': genre_type,
        'image': image,
        'review': [{
            'reviewer': reviewer,
            'rating': int(rating),
            'comments': comments
        }]
    }
    games.insert_one(game_form)
    return redirect(url_for("list_games"))


@app.route("/add_review/<game_id>", methods=["GET"])
def add_review(game_id):
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("addreview.html", game=game)


@app.route("/insert_review/<game_id>", methods=["POST"])
def insert_review(game_id):
    game = mongo.db.games
    reviewer = request.form['reviewer']
    rating = request.form['rating']
    comments = request.form['comments']

    game.update(
        {'_id': ObjectId(game_id)},
        {"$push": {"review": {
            "reviewer": reviewer,
            "rating": int(rating),
            "comments": comments
        }}}
    )
    return redirect(url_for("list_games"))


@app.route("/edit_game/<game_id>", methods=["GET"])
def edit_game(game_id):
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("editgame.html", game=game,
                           consoles=mongo.db.consoles.find(),
                           genres=mongo.db.genre.find())


@app.route("/update_game/<game_id>", methods=["POST"])
def update_game(game_id):
    PS4 = request.form["console_type_one"]
    XboxOne = request.form["console_type_two"]
    PC = request.form["console_type_three"]
    Nintendo_Switch = request.form["console_type_four"]
    genre_type = request.form['genre_type']
    image = request.form['image']

    if PS4 == "wrong":
        return redirect(url_for("page_not_found"))
    elif XboxOne == "wrong":
        return redirect(url_for("page_not_found"))
    elif PC == "wrong":
        return redirect(url_for("page_not_found"))
    elif Nintendo_Switch == "wrong":
        return redirect(url_for("page_not_found"))
    else:
        games = mongo.db.games
        games.update({'_id': ObjectId(game_id)},
                     {'$set': {'console_type': [{
                                "one": PS4,
                                "two": XboxOne,
                                "three": PC,
                                "four": Nintendo_Switch
                            }],
                            'genre_type': genre_type,
                            'image': image
                     }})
        return redirect(url_for("list_games"))


@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    game = mongo.db.games.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('list_games'))


@app.route("/sport")
def sport_genre():
    return render_template("filtergenre.html",
                           games=mongo.db.games.find({'genre_type': 'Sport'}))


@app.route("/FPS_genre")
def FPS_genre():
    return render_template("filtergenre.html",
                           games=mongo.db.games.find
                           ({'genre_type': 'First Person Shooter'}))


@app.route("/strategy_genre")
def strategy_genre():
    return render_template("filtergenre.html",
                           games=mongo.db.games.find
                           ({'genre_type': 'Strategy'}))


@app.route("/a_a_genre")
def a_a_genre():
    return render_template("filtergenre.html",
                           games=mongo.db.games.find
                           ({'genre_type': 'Action and Adventure'}))


@app.route("/other_genre")
def other_genre():
    return render_template("filtergenre.html",
                           games=mongo.db.games.find
                           ({'genre_type': 'Other'}))


@app.route("/racing_genre")
def racing_genre():
    return render_template("filtergenre.html",
                           games=mongo.db.games.find
                           ({'genre_type': 'Racing'}))


@app.route("/sandbox_genre")
def sandbox_genre():
    return render_template("filtergenre.html",
                           games=mongo.db.games.find
                           ({'genre_type': 'Sandbox'}))


@app.route("/404")
def page_not_found():
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
