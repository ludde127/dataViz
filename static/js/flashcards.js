class Flashcards {
    constructor(flash_data, subscribed_flashcards) {
        this.quiz_data = flash_data;
        this.quizzes = {};
        this.scores = {};
        this.subscribed = subscribed_flashcards;
    }
    nextCard(counter, correct) {

        document.getElementById("quiz-btn-next-"+counter).style.display = "none";

        console.assert(correct === -1 || correct === 1 || correct === 0);
        this.scores[counter][this.quizzes[counter]-1] = correct;
        document.getElementById("quiz-score-"+counter).innerHTML = this.amountCorrect(counter);

        let quiz = this.quiz_data[counter];
        let cards = quiz["cards"];
        document.getElementById("quiz-btn-"+counter).style.display = "initial";

        if (this.quizzes[counter] in cards) {
            document.getElementById("quiz-q-"+counter).innerHTML = cards[this.quizzes[counter]]["q"];
        } else {
            this.begin(counter);
            document.getElementById("quiz-progress-"+counter).innerHTML = 1+this.quizzes[counter];
            document.getElementById("quiz-btn-nextspan-"+counter).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+counter).style.display = "none";
            return this.nextCard(counter);
        }

        if (!(this.quizzes[counter]+1 in cards)) {
            document.getElementById("quiz-progress-"+counter).innerHTML = 1+this.quizzes[counter];

        }
        return false
    }

    begin(counter) {
        this.quizzes[counter] = 0;
        this.scores[counter] = {};
    }

    amountCorrect(counter) {
        let summed = 0;
        for (const elem of Object.values(this.scores[counter])) {
            if (!(elem === undefined)) {
                summed += elem;

            }
        }
        return summed
    }

    quizRunner(counter) {
        if (!(counter in this.quizzes)) {
            this.begin(counter);
            document.getElementById("quiz-btn-nextspan-"+counter).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+counter).style.display = "none";
        }
        let quiz = this.quiz_data[counter];

        let cards = quiz["cards"];

        if (this.quizzes[counter] in cards) {

            document.getElementById("quiz-btn-next-"+counter).style.display = "inline";
            document.getElementById("quiz-btn-"+counter).style.display = "none";
            document.getElementById("quiz-q-"+counter).innerHTML = "The answer is: " + '"' + cards[this.quizzes[counter]]["a"] + '"';

            this.quizzes[counter]+=1;
            if (!(this.quizzes[counter] in cards)) {

                document.getElementById("quiz-btn-nextspan-"+counter).style.display = "none";
                document.getElementById("quiz-btn-restartspan-"+counter).style.display = "inline";

            }
        }
    return false
}

    subscribeToggle(counter) {

    }
}