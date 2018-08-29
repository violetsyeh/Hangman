"use strict";

function displayWord(results) {
    var word = results;
    $('#word').html(word);
    $('#num-guesses-remain').html(' 6');
    console.log('secret word retrieved');
}

function getSecretWord() {
    $.get("/get-secret-word", displayWord);
}



$( document ).ready(getSecretWord);

