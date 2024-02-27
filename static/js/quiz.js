document.addEventListener('DOMContentLoaded', function() {
    // Extract the deckID from the URL
    const urlParts = window.location.pathname.split('/');
    const deckId = urlParts[urlParts.indexOf('deck') + 1];

    fetch(`/deck/${deckId}/quiz_data/`)
        .then(response => response.json())
        .then(data => {
            console.log(data.cards);
        });
});