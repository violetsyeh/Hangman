"use strict";

function displayUpdatedWord(result) {
    var updated_word = result;
    $('#update-word').html(updated_word);
    console.log('word updated');
}

function getUpdatedWord() {
    $.get('/check-guess', displayUpdatedWord);
    console.log("finished sending AJAX");
}

$('#updated-word').on('click', getUpdatedWord);