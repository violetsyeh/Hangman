"use strict";

function displayWord(results) {
    var word = results;
    $('#word').html(word);
}

function getSecretWord() {
    $.get('/get_secret_word', displayWord);
}

getSecretWord();