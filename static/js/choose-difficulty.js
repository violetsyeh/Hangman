"use strict";

function displayEditedWord(results) {
    var word = results;
    $('#word').html(word);
    $('#num-guesses-remain').html(' 6')
    console.log('secret word changed')
    $('#difficulty-field').val(' ')
}


function changeDifficulty(evt){
	evt.preventDefault();
	console.log("retrieving difficulty level");
	var difficulty = {
		"difficulty": $("#difficulty-field").val()
	};

	$.get("/change-difficulty", difficulty, displayEditedWord);
	console.log('word going to display');
	console.log(difficulty);
}






$("#change-difficulty").on('submit', changeDifficulty);