const LOCAL_URL = 'http://127.0.0.1:5000/';
const $form = $('#word-guess-form');
const $wordGuess = $('#word-guess').value;

async function handleWord(evt) {
    
    evt.preventDefault();
    const response = await axios({
        url: LOCAL_URL,
        method: 'POST',
        data: {wordAttempt: $wordGuess}     
    })
    .then((response) => {
        console.log(response);
      }, (error) => {
        console.log(error);
      });
    

}


$form.submit(handleWord)
