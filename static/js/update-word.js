"use strict";

function displayUpdatedWord(results) {
	console.log('start displaying updatedword');
	console.log(results)

    if (results['answer'] === 'incorrect'){
    	$('#word').html(results['updated_guess']);
    	console.log('word updated')
    	$('#incorrect-answer').html('That letter is not in the secret word');
    	$('#num-guesses-remain').html(results['num_guesses_remain']);
    	$('#incorrect-guesses').html(results['incorrect_guesses']);
    	$('#letter-tried-already').html('');

    } else if (results['answer'] === 'correct'){
    	$('#word').html(results['updated_guess']);
    	console.log('word updated')
    	$('#incorrect-answer').html('');
    	$('#num-guesses-remain').html(results['num_guesses_remain']);
    	$('#letter-tried-already').html('');

    } else if (results['game-status'] === 'game won'){
    	$('#word').html(results['updated_guess']);
    	$('#game-status-modal').modal();
    	$('#modal-text').html('You guessed the secret word correctly!');
    	$('#letter-tried-already').html('');

    } else if (results['game-status'] === 'game lost'){
    	$('#game-status-modal').modal()
    	$('#modal-text').html('You ran out of guesses, try again!');
    	$('#letter-tried-already').html('');
    	
    } else if (results['letter'] === 'tried already'){
    	$('#letter-tried-already').html("You already tried this letter.")
    };


    $("#updated-word")[0].reset();
}

function getUpdatedWord(evt) {
	evt.preventDefault();

	var formInput = {
		"letter": $("#letter-guess-field").val()
	};

	// console.log(formInput);

	console.log('start getting updatedword');
    $.get("/check-guess", formInput, displayUpdatedWord);
    console.log("finished sending AJAX");
}

$( "#updated-word" ).on('submit', getUpdatedWord);
