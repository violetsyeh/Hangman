"use strict";

function displayUpdatedWord(results) {
	console.log('start displaying updatedword');
	console.log(results)
    // $('#word').html(results['updated_guess']);
    // console.log('word updated');

    if (results['answer'] === 'incorrect'){
    	$('#word').html(results['updated_guess']);
    	$('#incorrect-answer').html('That letter is not in the secret word');
    } else if (results['answer'] === 'correct'){
    	$('#word').html(results['updated_guess']);
    	$('#incorrect-answer').html('');
    };
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