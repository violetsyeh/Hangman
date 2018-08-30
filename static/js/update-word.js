"use strict";

function displayUpdatedWord(results) {
	// console.log('start displaying updatedword');
	console.log(results);

    if (results['answer'] === 'incorrect'){
    	$('#word').html(results['updated_guess']);
    	// console.log('word updated');
    	$('#incorrect-answer').html('That letter is not in the secret word');
    	$('#num-guesses-remain').html(results['num_guesses_remain']);
    	$('#incorrect-guesses').html(results['incorrect_guesses']);
    	$('#letter-tried-already').html('');

    } else if (results['answer'] === 'correct'){
    	$('#word').html(results['updated_guess']);
    	// console.log('word updated');
    	$('#incorrect-answer').html('');
    	$('#num-guesses-remain').html(results['num_guesses_remain']);
    	$('#letter-tried-already').html('');

    } else if (results['game_status'] === 'game won'){
    	$('#word').html(results['updated_guess']);
    	$('#game-status-modal').modal();
    	$('#modal-text').html('You guessed the secret word correctly!');
    	$('#letter-tried-already').html('');

    } else if (results['game_status'] === 'game lost'){
    	$('#game-status-modal').modal();
    	$('#modal-text').html('You ran out of guesses, try again!');
    	$('#letter-tried-already').html('');

    } else if (results['guess'] === 'tried already'){
    	$('#letter-tried-already').html("You already tried this letter.")
    
    } else if (results['whole_word_guess'] === 'incorrect'){
        $('#word').html(results['updated_guess']);
        $('#num-guesses-remain').html(results['num_guesses_remain']);
        $('#num-guesses-remain').html(results['num_guesses_remain']);
        $('#incorrect-guesses').html(results['incorrect_guesses']);
    }   


    $("#updated-word")[0].reset();
}

// function displayIfSolvedWord(results){
//     if (results['game_status'] === 'game won')
// }


function getUpdatedWord(evt) {
	evt.stopImmediatePropagation();
	evt.preventDefault();

	var letterInput = {
		"letter": $("#letter-guess-field").val()

	};

    var wordInput = {
        "word": $("#full-word-field").val()
    }
	console.log(letterInput);
    console.log(wordInput);

	console.log('start getting updatedword');
    if (letterInput["letter"] != ""){
        $.get("/check-guess", letterInput, displayUpdatedWord);
    }
    else if (wordInput["word"] != ""){
        $.get("/check-whole-word", wordInput, displayUpdatedWord);
    }
}



$("#updated-word").on('submit', getUpdatedWord);

