let id_end = "user-subscribed-cards";
class CardHolder {
    constructor(card_array) {
        // card_array holds array of these {"q": card.value["question"], "a": card.value["answer"],
        //      "id": card.id, "block_id": string_block_id, "notepage_id": notepage_id,
        //      "weight": weight, "times_displayed": times_displayed, "score": score}
        this.card_id_to_card = {};
        for (const card of card_array) {
            this.card_id_to_card[card["id"]] = card;
        }

        this.past_card = card_array[0];

        this.past_cards = [];
    }

    next_card() {
        // Only doing O(n) linear search for lowest weight, because js.
        // If they have a high weight they shall be shown.
        let largest = -Infinity;
        let result = undefined;
        for (const card of Object.values(this.card_id_to_card)) {
            if (card["weight"] > largest && !this.past_cards.includes(card)) {
                result = card;
                largest = card["weight"];
            }
        }
        this.past_card = result;
        this.past_cards.push(result);
        if (this.past_cards.length > 5 || this.past_cards > this.card_id_to_card.length / 3) {
            this.past_cards.shift()
        }
        return result
    }

    update_card(new_card_dict) {
        console.log(new_card_dict);
        let to_change = this.card_id_to_card[new_card_dict["id"]];
        console.log(to_change);

        to_change["weight"] = new_card_dict["weight"];
        to_change["score"] = new_card_dict["score"]
        to_change["times_displayed"] = new_card_dict["times_displayed"]

        this.card_id_to_card[new_card_dict["id"]] = to_change; // This might be dumb to reassign but cant be bothered to find out.
    }
}

class UserFlashcards {
    constructor(flash_card_list) {
        this.flashcards = flash_card_list;
        this.scores = {};
        console.log(this.flashcards);
        console.log(typeof this.flashcards)
        this.card_holder = new CardHolder(flash_card_list);

        this.current_index = 0;
    }
    nextCard(correct) {
        let past_card = this.card_holder.past_card;
        let card = this.card_holder.next_card();

        document.getElementById("quiz-btn-next-"+id_end).style.display = "none";

        this.scores[this.current_index-1] = correct;

        async function interactionChange(past_card) {
            const response = await fetch(`/api-v2/change/flashcard-interaction/?page=${past_card["notepage_id"]}&flashcards=${past_card["block_id"]}&flashcard=${past_card["id"]}&score=${correct}`);
            return await response.json()
        }


        interactionChange(past_card).then(json => {
            console.log(json);
            this.card_holder.update_card(json);
        })


        document.getElementById("quiz-score-"+id_end).innerHTML = this.amountCorrect();

        document.getElementById("quiz-btn-"+id_end).style.display = "initial";

        if (card) {
            document.getElementById("quiz-q-"+id_end).innerHTML = card["q"];
        } else {
            this.begin();
            document.getElementById("quiz-progress-"+id_end).innerHTML = 1+this.current_index;
            document.getElementById("quiz-btn-nextspan-"+id_end).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+id_end).style.display = "none";
            return this.nextCard();
        }

        if (card) {
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
        if (this.current_index===0) {
            this.begin();
            document.getElementById("quiz-btn-nextspan-"+id_end).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-"+id_end).style.display = "none";
        }

        let card = this.card_holder.past_card;

        document.getElementById("quiz-btn-next-"+id_end).style.display = "inline";
        document.getElementById("quiz-btn-"+id_end).style.display = "none";
        document.getElementById("quiz-q-"+id_end).innerHTML = "The answer is: " + '"' + card["a"] + '"';

        this.current_index+=1;


        return false
    }
}