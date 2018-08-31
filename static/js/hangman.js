"use strict";


function displayWord(results) {
    var word = results;
    $('#word').html(word);
    $('#num-guesses-remain').html(' 6');
}


function getSecretWord() {
    $.get("/get-secret-word", displayWord);
}


function displayEditedWord(results) {
    var word = results;
    $('#word').html(word);
    $('#num-guesses-remain').html(' 6')
    $('#difficulty-field').val(' ')
}


function changeDifficulty(evt){
	evt.preventDefault();

	var difficulty = {
		"difficulty": $("#difficulty-field").val()
	};

	$.get("/change-difficulty", difficulty, displayEditedWord);
}


$("#play-again").on("click", function(){
            location.reload();
        });


function displayUpdatedWord(results) {

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


function getUpdatedWord(evt) {

	evt.stopImmediatePropagation();
	evt.preventDefault();

	var letterInput = {
		"letter": $("#letter-guess-field").val()

	};

    var wordInput = {
        "word": $("#full-word-field").val()
    }

    if (letterInput["letter"] != ""){
        $.get("/check-guess", letterInput, displayUpdatedWord);
    }
    
    else if (wordInput["word"] != ""){
        $.get("/check-whole-word", wordInput, displayUpdatedWord);
    }
}




$("#change-difficulty").on('submit', changeDifficulty);
$("#updated-word").on('submit', getUpdatedWord);
$( document ).ready(getSecretWord);