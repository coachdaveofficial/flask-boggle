const LOCAL_URL = 'http://127.0.0.1:5000/';
const $form = $('#word-guess-form');
const $responseDiv = $('#response');
const $scoreBoard = $('#score-board')
const guessedWords = [];
const $timerHTML = $('.timer');
const $startTimerButton = $('#start-timer');
const $highScore = $('#high-score');
const $numPlays = $('#num-plays');



// get length of word and add it to scoreboard HTML
function updateScore(word) {
    let newScore
    let test = $scoreBoard.text()
     if (test) {
         let currentScore = parseInt($scoreBoard.text());
         newScore = currentScore
     } else {
         let currentScore = 0;
         newScore = currentScore
     }
     let points = word.length;
     newScore += points;
     $scoreBoard.text(newScore)
 }
 // grab current score and compare to high score stored in flask session
async function updateHighScore() {
    let currentScore = $scoreBoard.text();
    const response = await axios.get(LOCAL_URL + '/new-score', {params: {score: currentScore}})
    console.log(response);
    $highScore.text(response.data['highscore']);
    $numPlays.text(response.data['num_plays']);
}
function updateNumPlays() {
    
}

// start game and timer for game and show/hide form if game over/restarted
// duration = seconds, display = jquery element
function startTimer(duration, display) {
    $form.show()
    $startTimerButton.text('Restart Game');
    // $startTimerButton.prop('disabled', true)
    display.text('Ready!')
    let counter = duration;
    const interval = setInterval(function(){
        display.text(counter)
        counter--
        // if game is over
        if (counter < 0) {
            console.log('clear?')
            clearInterval(interval);
            $form.hide();
            updateHighScore();
            $scoreBoard.text('');
            $responseDiv.hide();
        }
    }, 1000)    
}

$startTimerButton.on('click', () => startTimer(60, $timerHTML))

// check response from word submission and pass guessed word to score updater
function checkValidWord(guessedWord,res) {
    
    if (res === 'ok') {
        updateScore(guessedWord);
        guessedWords.push(guessedWord);
        return `${guessedWord} is a valid word!`;
    } else if (res === "not-on-board") {
        return `'${guessedWord}' does not exist on board`;
    } else {
        return `'${guessedWord}' is not a valid word`;
    }
}

// 
async function wordSubmit(evt) {
    
    evt.preventDefault();
    let wordInput = $('#word-guess');
    let wordGuess = wordInput.val();
    if (guessedWords.includes(wordGuess)) {
        $responseDiv.text(`'${wordGuess}' has already been used`)
    } else {
        const response = await axios.get(LOCAL_URL + '/word-check', {params: {word: wordGuess}})
        console.log(response.data['result'])
        let result = checkValidWord(wordGuess, response.data['result']);
        $responseDiv.show();

        // set background-color
        $responseDiv.css('background-color', 'blueviolet')


        $responseDiv.text(result);
        wordInput.val('');
    }
}


$form.submit(wordSubmit)


$(function() {
    console.log( "ready!" );
    updateHighScore();
});