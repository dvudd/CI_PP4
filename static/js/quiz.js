document.addEventListener('DOMContentLoaded', function() {
    // Load the Card data
    const cardsData = JSON.parse(document.getElementById('cards-data').textContent);
    console.log(cardsData); // REMOVE THIS
    
    let currentCardIndex = 0;

    // Navigation button states
    function updateButtonStates() {
        // Handle the previous button state
        if (currentCardIndex <= 0) {
            document.getElementById('prev-question-btn').classList.add('visually-hidden');
        } else {
            document.getElementById('prev-question-btn').classList.remove('visually-hidden');
        }
        
        // Handle the next button state
        if (currentCardIndex >= cardsData.length - 1) {
            document.getElementById('next-question-btn').classList.add('visually-hidden');
        } else {
            document.getElementById('next-question-btn').classList.remove('visually-hidden');
        }
    }

    // Touch
    let touchStart = 0;
    let touchEnd = 0;
    const questionArea = document.getElementById('question-area');

    function swipe() {
        if (touchEnd < touchStart) {
            // Swipe Left - Show Next Question
            document.getElementById('next-question-btn').click();
        }
        if (touchEnd > touchStart) {
            // Swipe Right - Show Previous Question
            document.getElementById('prev-question-btn').click();
        }
    }

    questionArea.addEventListener('touchstart', e => {
        touchStart = e.changedTouches[0].screenX;
    });

    questionArea.addEventListener('touchend', e => {
        touchEnd = e.changedTouches[0].screenX;
        swipe();
    });

    // Show the question
    function displayQuestion() {
        const card = cardsData[currentCardIndex];
        // Display the question image, if there is one
        const questionImage = document.getElementById('question-image');
        if (card.question_image) {
            document.getElementById("question-image").classList.remove("visually-hidden");
            questionImage.src = card.question_image;
        } else {
            document.getElementById("question-image").classList.add("visually-hidden");
        }
        if (card.question) {
            document.getElementById("question-text").classList.remove("visually-hidden");
            document.getElementById('question-text').textContent = card.question;
        } else {
            document.getElementById("question-text").classList.add("visually-hidden");
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
            document.getElementById('answer-area').style.display = 'none';
         }
    });

    displayQuestion();
});