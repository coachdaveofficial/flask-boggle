from xml.etree.ElementTree import tostring
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
    # session['scores'] = []
    

    return render_template('index.html', board=session["board"])

@app.route('/word-check')
def word_check():
    word = request.args['word']
    board = session["board"]
    session.get('high_score', 0)
    session.get('num_plays', 0)
    

    response = boggle_game.check_valid_word(board, word)

    return jsonify(result = response)

@app.route('/new-score/')
def new_score():
    new_score = request.args['score']
    num_plays = session.get('num_plays', 0)
    num_plays += 1
    session['num_plays'] = num_plays
    # if no current score, set score to 0
    if new_score == '':
        new_score = 0
    high_score = max(int(new_score), int(session.get('high_score', 0)))
    session['high_score'] = high_score


    print(session['high_score'])

    

    return jsonify(score = new_score, highscore = high_score, num_plays = num_plays)

