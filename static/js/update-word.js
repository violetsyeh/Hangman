"use strict";

function displayUpdatedWord(results) {
	console.log('start display updatedword');
	console.log(results)
    var updated_word = results;
    $('#word').html(updated_word);
    console.log('word updated');
}

function getUpdatedWord(evt) {
	evt.preventDefault();

	var formInput = {
		"letter": $("#letter-guess-field").val()
	};

	console.log(formInput);

	console.log('start getting updatedword');
    $.get("/check-guess", formInput, displayUpdatedWord);
    console.log("finished sending AJAX");
}

$( "#updated-word" ).on('submit', getUpdatedWord);