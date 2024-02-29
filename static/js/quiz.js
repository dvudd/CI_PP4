document.addEventListener('DOMContentLoaded', function() {
    // Load the Card data
    const cardsData = JSON.parse(document.getElementById('cards-data').textContent);
    console.log(cardsData); // REMOVE THIS
    
    let currentCardIndex = 0;

    // Navigation button states
    function updateButtonStates() {
        // Handle the previous button state
        if (currentCardIndex <= 0) {
            document.getElementById('prev-question-btn').classList.add('disabled');
        } else {
            document.getElementById('prev-question-btn').classList.remove('disabled');
        }
        
        // Handle the next button state
        if (currentCardIndex >= cardsData.length - 1) {
            document.getElementById('next-question-btn').classList.add('disabled');
        } else {
            document.getElementById('next-question-btn').classList.remove('disabled');
        }
    }

    // Show the question
    function displayQuestion() {
        const card = cardsData[currentCardIndex];
        document.getElementById('question-text').textContent = card.question;
        // Display the question image, if there is one
        const questionImage = document.getElementById('question-image');
        if (card.question_image) {
            questionImage.src = card.question_image;
            questionImage.style.display = '';
        } else {
            questionImage.style.display = 'none';
        }
        updateButtonStates();
    }

    // Show the answer
    function revealAnswer() {
        const card = cardsData[currentCardIndex];
        document.getElementById('answer-text').textContent = card.answer;
        // Display the answer image, if there is one
        const answerImage = document.getElementById('answer-image');
        if (card.answer_image) {
            answerImage.src = card.answer_image;
            answerImage.style.display = '';
        } else {
            answerImage.style.display = 'none';
        }
        document.getElementById('answer-area').style.display = '';
    }

    // Event listener for reveal button
    document.getElementById('reveal-answer-btn').addEventListener('click', revealAnswer);
    
    // Event listener for next question button
    document.getElementById('next-question-btn').addEventListener('click', function() {
        currentCardIndex += 1;
        if (currentCardIndex < cardsData.length) {
            displayQuestion();
            document.getElementById('answer-area').style.display = 'none';
        };
    });

    // Event listener for previous question button
    document.getElementById('prev-question-btn').addEventListener('click', function() {
         if (currentCardIndex > 0) {
            currentCardIndex -= 1;
            displayQuestion();
         }
    });

    displayQuestion();
});