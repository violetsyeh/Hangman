"use strict";

function displayWord(results) {
    var word = results;
    $('#word').html(word);
    console.log('secret word retrieved')
}

function getSecretWord() {
    $.get('/get-secret-word', displayWord);
}

$( document ).ready(getSecretWord);