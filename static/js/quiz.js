document.addEventListener('DOMContentLoaded', function() {
    // Load the Card data
    const cardsData = JSON.parse(document.getElementById('cards-data').textContent);

    // Shuffle the order of the questions
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
          // Generate random index
          const j = Math.floor(Math.random() * (i + 1));
          // Swap elements at indices i and j
          [array[i], array[j]] = [array[j], array[i]];
        }
      }
     shuffle(cardsData);

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

    // Touch Controls
    let touchStart = 0;
    let touchEnd = 0;
    const questionArea = document.getElementById('quiz-card');
    const minimumDistance = 75;

    function swipe() {
        let distance = touchEnd - touchStart;
        // If the swipe distance is less than the minimum, don't do anything
        if (Math.abs(distance) < minimumDistance) {
            return;
        }

        if (distance < 0) {
            // Swipe Left - Show Next Question
            document.getElementById('next-question-btn').click();
        } else if (distance > 0) {
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

    // Flip the card
    document.getElementById('quiz-card').addEventListener('click', function() {
        document.getElementById('quiz-card').classList.toggle('flip');
    });

    // Show the question
    function displayQuestion() {
        const card = cardsData[currentCardIndex];
        const questionImage = document.getElementById('question-image');
        const answerImage = document.getElementById('answer-image');
        // Display the question image, if there is one
        if (card.question_image) {
            questionImage.src = card.question_image;
            document.getElementById("question-image-area").classList.remove("visually-hidden");
            document.getElementById("question-text-area").classList.remove("card-row-full");
        } else {
            document.getElementById("question-image-area").classList.add("visually-hidden");
            document.getElementById("question-text-area").classList.add("card-row-full");
        }
        // Display the question text, if there is one
        if (card.question) {
            document.getElementById("question-text").textContent = card.question;
            document.getElementById("question-text-area").classList.remove("visually-hidden");
            document.getElementById("question-image-area").classList.remove("card-row-full");
        } else {
            document.getElementById("question-text-area").classList.add("visually-hidden");
            document.getElementById("question-image-area").classList.add("card-row-full");
        }
        // Display the answer image, if there is one
        if (card.answer_image) {
            answerImage.src = card.answerimage;
            document.getElementById("answer-image-area").classList.remove("visually-hidden");
            document.getElementById("answer-text-area").classList.remove("card-row-full");
        } else {
            document.getElementById("answer-image-area").classList.add("visually-hidden");
            document.getElementById("answer-text-area").classList.add("card-row-full");
        }
        // Display the answer text, if there is one
        if (card.answer) {
            document.getElementById("answer-text").textContent = card.answer;
            document.getElementById("answer-text-area").classList.remove("visually-hidden");
            document.getElementById("answer-image-area").classList.remove("card-row-full");
        } else {
            document.getElementById("answer-text-area").classList.add("visually-hidden");
            document.getElementById("answer-image-area").classList.add("card-row-full");
        }
        updateButtonStates();
    }
  
    /**
     * Sleep function
     * @param {time} ms 
     * CREDIT: https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
     */
    function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Event listener for next question button
    document.getElementById('next-question-btn').addEventListener('click', async function() {
        if (currentCardIndex < cardsData.length) {
            currentCardIndex += 1;
            if (document.getElementById('quiz-card').classList.contains('flip')) {
                document.getElementById('quiz-card').classList.remove('flip');
                await sleep(200);
                displayQuestion();
            }
            else {
                document.getElementById('quiz-card').classList.add('fade-out-left');
                await sleep(200);
                document.getElementById('quiz-card').classList.remove('fade-out-left');
                document.getElementById('quiz-card').classList.remove('flip');
                document.getElementById('quiz-card').classList.add('fade-in-left');
                displayQuestion();
                await sleep(500);
                document.getElementById('quiz-card').classList.remove('fade-in-left');
            }
        }
    });

    // Event listener for previous question button
    document.getElementById('prev-question-btn').addEventListener('click', async function() {
         if (currentCardIndex > 0) {
            currentCardIndex -= 1;
            if (document.getElementById('quiz-card').classList.contains('flip')) {
                document.getElementById('quiz-card').classList.remove('flip');
                await sleep(200);
                displayQuestion();
            }
            else {
                document.getElementById('quiz-card').classList.add('fade-out-right');
                await sleep(200);
                document.getElementById('quiz-card').classList.remove('fade-out-right');
                document.getElementById('quiz-card').classList.remove('flip');
                document.getElementById('quiz-card').classList.add('fade-in-right');
                displayQuestion();
                await sleep(500);
                document.getElementById('quiz-card').classList.remove('fade-in-right');
            }
         }
    });

    displayQuestion();
});