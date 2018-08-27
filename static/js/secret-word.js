"use strict";

function displayWord(results) {
    var word = results;
    $('#word').html(word);
}

function getSecretWord() {
    $.get('/get-secret-word', displayWord);
}

$( document ).ready(getSecretWord);