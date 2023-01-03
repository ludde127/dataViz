
class Flashcards {
    constructor(flash_data, page_id, subscribed_cards) {
        this.quiz_data = flash_data;
        this.quizzes = {};
        this.scores = {};
        this.page_id = page_id;
        this.subscribed_cards = subscribed_cards;
    }
    nextCard(block_id, correct) {
        let past_card = this.quiz_data[block_id]["cards"][this.quizzes[block_id]-1]
        let quiz = this.quiz_data[block_id];

        let cards = quiz["cards"];

        document.getElementById("quiz-btn-next-"+block_id).style.display = "none";

        this.scores[block_id][this.quizzes[block_id]-1] = correct;
        if (!(past_card === undefined))
        {
            fetch(`/api-v2/change/flashcard-interaction/?page=${this.page_id}&flashcards=${block_id}&flashcard=${past_card["id"]}&score=${correct}`)
        }
        document.getElementById("quiz-score-"+block_id).innerHTML = this.amountCorrect(block_id);

        document.getElementById("quiz-btn-"+block_id).style.display = "initial";

        if (this.quizzes[block_id] in cards) {
            document.getElementById("quiz-q-"+block_id).innerHTML = cards[this.quizzes[block_id]]["q"];
        } else {
            this.begin(block_id);
            document.getElementById("quiz-progress-"+block_id).innerHTML = 1+this.quizzes[block_id];
            document.getElementById("quiz-btn-nextspan-"+block_id).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+block_id).style.display = "none";
            return this.nextCard(block_id);
        }

        if (!(this.quizzes[block_id]+1 in cards)) {
            document.getElementById("quiz-progress-"+block_id).innerHTML = 1+this.quizzes[block_id];

        }
        return false
    }

    begin(block_id) {
        this.quizzes[block_id] = 0;
        this.scores[block_id] = {};
    }

    amountCorrect(block_id) {
        let summed = 0;
        for (const elem of Object.values(this.scores[block_id])) {
            if (!(elem === undefined)) {
                summed += elem;

            }
        }
        return summed
    }

    quizRunner(block_id) {
        if (!(block_id in this.quizzes)) {
            this.begin(block_id);
            document.getElementById("quiz-btn-nextspan-"+block_id).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+block_id).style.display = "none";
        }
        let quiz = this.quiz_data[block_id];

        let cards = quiz["cards"];

        if (this.quizzes[block_id] in cards) {

            document.getElementById("quiz-btn-next-"+block_id).style.display = "inline";
            document.getElementById("quiz-btn-"+block_id).style.display = "none";
            document.getElementById("quiz-q-"+block_id).innerHTML = cards[this.quizzes[block_id]]["a"];

            this.quizzes[block_id]+=1;
            if (!(this.quizzes[block_id] in cards)) {

                document.getElementById("quiz-btn-nextspan-"+block_id).style.display = "none";
                document.getElementById("quiz-btn-restartspan-"+block_id).style.display = "inline";

            }
        }
    return false
}

    subscribeToggle(block_id) {
        if (!(this.page_id === "None")) { // Am in user flashcards page
            if (this.subscribed_cards.includes(block_id)) {
                //Unsubscribe
                // http://127.0.0.1:8000/api-v2/change/subscribe/?page=11&flashcards=47b3d79e-189a-4bd8-99b1-45e2d75106f9
                fetch(`/api-v2/change/unsubscribe/?page=${this.page_id}&flashcards=${block_id}`).then(function (response) {
                    if (response.status == 200) {
                        document.getElementById("quiz-subscribe-span-" + block_id).innerHTML = "Subscribe";
                    }
                });
                const index = this.subscribed_cards.indexOf(block_id);
                if (index > -1) { // only splice array when item is found
                    this.subscribed_cards.splice(index, 1); // 2nd parameter means remove one item only
                }

            } else {
                fetch(`/api-v2/change/subscribe/?page=${this.page_id}&flashcards=${block_id}`).then(function (response) {
                    if (response.status == 200) {
                        document.getElementById("quiz-subscribe-span-" + block_id).innerHTML = "Unsubscribe";
                    }
                });
                this.subscribed_cards.push(block_id);
            }
        }
    }
}