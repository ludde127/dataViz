let id_end = "user-subscribed-cards";

class UserFlashcards {
    constructor(flash_card_list) {
        this.flashcards = flash_card_list;
        this.scores = {};
        console.log(this.flashcards);
        console.log(typeof this.flashcards)

        this.current_index = 0;
    }
    nextCard(correct) {
        let past_card = this.flashcards[this.current_index-1]
        let card = this.flashcards[this.current_index]

        document.getElementById("quiz-btn-next-"+id_end).style.display = "none";

        this.scores[this.current_index-1] = correct;
        if (!(past_card === undefined))
        {
            fetch(`/api-v2/change/flashcard-interaction/?page=${past_card["notepage_id"]}&flashcards=${past_card["block_id"]}&flashcard=${past_card["id"]}&score=${correct}`)
        }
        document.getElementById("quiz-score-"+id_end).innerHTML = this.amountCorrect();

        document.getElementById("quiz-btn-"+id_end).style.display = "initial";

        if (this.current_index < this.flashcards.length) {
            document.getElementById("quiz-q-"+id_end).innerHTML = card["q"];
        } else {
            this.begin();
            document.getElementById("quiz-progress-"+id_end).innerHTML = 1+this.current_index;
            document.getElementById("quiz-btn-nextspan-"+id_end).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+id_end).style.display = "none";
            return this.nextCard();
        }

        if (this.current_index+1 < this.flashcards.length) {
            document.getElementById("quiz-progress-"+id_end).innerHTML = 1+this.current_index;

        }
        return false
    }

    begin() {
        this.scores = {};
        this.current_index = 0;
    }

    amountCorrect() {
        let summed = 0;
        for (const elem of Object.values(this.scores)) {
            if (!(elem === undefined)) {
                summed += elem;

            }
        }
        return summed
    }

    quizRunner() {
        if (this.current_index > this.flashcards.length || this.current_index===0) {
            this.begin();
            document.getElementById("quiz-btn-nextspan-"+id_end).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+id_end).style.display = "none";
        }

        if (this.current_index < this.flashcards.length) {
            let card = this.flashcards[this.current_index]

            document.getElementById("quiz-btn-next-"+id_end).style.display = "inline";
            document.getElementById("quiz-btn-"+id_end).style.display = "none";
            document.getElementById("quiz-q-"+id_end).innerHTML = "The answer is: " + '"' + card["a"] + '"';

            this.current_index+=1;
            if (this.current_index > this.flashcards.length) {

                document.getElementById("quiz-btn-nextspan-"+id_end).style.display = "none";
                document.getElementById("quiz-btn-restartspan-"+id_end).style.display = "inline";

            }
        }
        return false
    }
}