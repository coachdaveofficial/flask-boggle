from flask import Flask, request, render_template, session
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_boggle_game"
toolbar = DebugToolbarExtension(app)


boggle_game = Boggle()

@app.route('/')
def home_page():
    session["board"] = boggle_game.make_board()
    

    return render_template('index.html', board=session["board"])

@app.route('/word-check', methods=["POST"])
def word_check():
    word = request.args['word-guess']

    return render_template('index.html', board=session["board"], word='test')

# def handle_word(board, word):
#    result = boggle_game(board, word)
#    return result