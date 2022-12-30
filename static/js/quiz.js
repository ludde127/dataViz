function validateAnswer(input, cardElement) {
    input = String(input).trim();
    cardElement = String(cardElement).trim();
    if (input === cardElement) {
        return true
    } else if (input.toLowerCase() === cardElement.toLowerCase()) {
        return true
    }
    return false
}

class Quizzes {
    constructor(quiz_data) {
        this.quiz_data = quiz_data;
        this.quizzes = {};
        this.scores = {};
    }

    nextCard(counter) {
        document.getElementById("quiz-btn-next-"+counter).style.display = "none";


        let quiz = this.quiz_data[counter];
        let cards = quiz["cards"];
        document.getElementById("quiz-btn-"+counter).style.display = "initial";
        for (const div of document.getElementsByClassName("succ-fail-"+counter)) {
                let divClasses = div.classList;
                divClasses.remove("failure-quiz");

                divClasses.remove("correct-quiz")
            }

        if (this.quizzes[counter] in cards) {
            document.getElementById("quiz-q-"+counter).innerHTML = cards[this.quizzes[counter]]["q"];
        } else {
            this.begin(counter);
            document.getElementById("quiz-progress-"+counter).innerHTML = 1+this.quizzes[counter];

            return this.nextCard(counter);
        }

        if (!(this.quizzes[counter]+1 in cards)) {
            document.getElementById("quiz-progress-"+counter).innerHTML = 1+this.quizzes[counter];

        }
        return false
    }

    begin(counter) {
        this.quizzes[counter] = 0;
        this.scores[counter] = 0;
    }

    quizRunner(counter) {
        if (!(counter in this.quizzes)) {
            this.begin(counter);
        }
        let quiz = this.quiz_data[counter];
        let input_element = document.getElementById("quiz-input-field-"+counter);
        let input = undefined;
        if (!(input_element === undefined)) {
            input = input_element.value;
        }
        let cards = quiz["cards"];

        if (this.quizzes[counter] in cards) {
            if (!(input === null)) {
                let card = cards[this.quizzes[counter]];
                let correct = validateAnswer(input, card["a"]);
                for (const div of document.getElementsByClassName("succ-fail-"+counter)) {
                let divClasses = div.classList;
                if (correct) {
                    divClasses.remove("failure-quiz");
                    divClasses.add("correct-quiz")
                } else {
                    divClasses.add("failure-quiz");
                    divClasses.remove("correct-quiz")
                }
                }
                document.getElementById("quiz-btn-"+counter).style.display = "none";
                if (correct) {
                    this.scores[counter]= this.scores[counter] + parseInt(card["score"]);
                    document.getElementById("quiz-q-"+counter).innerHTML = "You answered correctly!";
                } else {
                    document.getElementById("quiz-q-"+counter).innerHTML = "You answered incorrectly("+'"'+input+'"'+") correct was " + '"' + cards[this.quizzes[counter]]["a"] + '"';
                }
            }


            document.getElementById("quiz-btn-next-"+counter).style.display = "inline";

            this.quizzes[counter]+=1;
            document.getElementById("quiz-score-"+counter).innerHTML = this.scores[counter];
            if (!(this.quizzes[counter] in cards)) {
                let passed = this.scores[counter] >= quiz["passing_score"];
                if (passed) {
                    let temp = document.getElementById("quiz-q-"+counter).innerText;
                    document.getElementById("quiz-q-"+counter).innerHTML = temp + " | You Passed!";
                }
                document.getElementById("quiz-btn-nextspan-"+counter).innerHTML = "Slut på kort, starta om!";
            } else {
                document.getElementById("quiz-btn-nextspan-"+counter).innerHTML = "Next";
            }
        }
    return false
}
}