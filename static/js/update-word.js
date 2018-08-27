"use strict";

function displayUpdatedWord(result) {
	console.log('start display updatedword');
    var updated_word = result['letter-guess'];
    $('#word').html(updated_word);
    console.log('word updated');
}

function getUpdatedWord(evt) {
	evt.preventDefault();

	var formInput = {
		"letter-guess": $("#letter-guess-field").val()
	};

	console.log(formInput);

	console.log('start getting updatedword');
    $.get('/check-guess', formInput, displayUpdatedWord);
    console.log("finished sending AJAX");
}

$( "#updated-word" ).on('submit', getUpdatedWord);