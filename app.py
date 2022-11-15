from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_boggle_game"
toolbar = DebugToolbarExtension(app)


boggle_game = Boggle()

@app.route('/')
def home_page():
    session["board"] = boggle_game.make_board()
    session['scores'] = []
    

    return render_template('index.html', board=session["board"])

@app.route('/word-check')
def word_check():
    word = request.args['word']
    board = session["board"]
    

    response = boggle_game.check_valid_word(board, word)

    return jsonify(result = response)

@app.route('/new-score/')
def new_score():
    new_score = request.args['score']
    session['new_score'] = new_score
    return jsonify(score = new_score)
