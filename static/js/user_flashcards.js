import toggleShow from "./utils.js";

let id_end = "user-subscribed-cards";

function shuffle(array) {
    //https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
    return array.map(value => ({value, sort: Math.random()}))
        .sort((a, b) => a.sort - b.sort)
        .map(({value}) => value)
}

class CardHolder {
    constructor(card_array, first_card) {
        // card_array holds array of these {"q": card.value["question"], "a": card.value["answer"],
        //      "id": card.id, "block_id": string_block_id, "notepage_id": notepage_id,
        //      "weight": weight, "times_displayed": times_displayed, "score": score}
        this.card_id_to_card = {};
        for (const card of card_array) {
            this.card_id_to_card[card["id"]] = card;
        }

        this.past_card = first_card;
        this.past_cards = [first_card,];
        //console.log(first_card)
    }


    next_card() {
        // Only doing O(n) linear search for lowest weight, because js.
        // If they have a high weight they shall be shown.
        let largest = -Infinity;
        let result = undefined;

        // May have to instead sort two times as this may lock in a card with a rather low score.
        let list_of_cards = Object.values(this.card_id_to_card).sort((a, b) => a["last_displayed_float"] - b["last_displayed_float"]);

        for (const card of list_of_cards) {
            // I HAVE NO CLUE WHY I NEED TO CHECK THAT THIS CARD IS NOT EQUAL TO LAST, IT SHOULD BE LAST IN QUEUE.
            // MAYBE THE ASYNC DO NOT HAVE TIME TO BE COMPLETED?
            let weight = card["weight"];

            let seconds_since_shown = Date.now() / 1000 - card["last_displayed_float"];
            if (seconds_since_shown < 60 * 60) {
                weight = weight - (60 * 60 - seconds_since_shown) / 15; // To make it less likely for a card to show up all the time
            }
            weight -= card["times_displayed"]
            if (!(card === this.past_card) && card["times_displayed"] === 0) {
                result = card;
                break
            } else if (weight > largest && (!(card === this.past_card))) {
                result = card;
                largest = card["weight"];
            }
        }
        this.past_card = result;
        this.past_cards.push(result["id"]);

        return result
    }


    update_card(new_card_dict) {
        //console.log("New card");
        //console.log(this.card_id_to_card[new_card_dict["id"]]["last_displayed_float"]);
        this.card_id_to_card[new_card_dict["id"]]["weight"] = new_card_dict["weight"];
        this.card_id_to_card[new_card_dict["id"]]["score"] = new_card_dict["score"];
        this.card_id_to_card[new_card_dict["id"]]["times_displayed"] = new_card_dict["times_displayed"];
        this.card_id_to_card[new_card_dict["id"]]["last_displayed_float"] = new_card_dict["last_displayed_float"];
        //console.log(this.card_id_to_card[new_card_dict["id"]]["last_displayed_float"]);

        //console.log("Should not be same");
    }
}

export default class UserFlashcards {
    constructor(flash_card_list, first_card) {
        this.flashcards = flash_card_list;
        this.scores = {};
        console.log(this.flashcards);
        console.log(typeof this.flashcards)
        this.card_holder = new CardHolder(flash_card_list, first_card);

        this.current_index_unique = 0;
        this.current_index = 0;
        this.cardsSeen = [first_card["id"],];
    }

    nextCard(correct) {
        let past_card = this.card_holder.past_card;
        let card = this.card_holder.next_card();

        toggleShow("quiz-btn-next-" + id_end);

        this.scores[this.current_index - 1] = correct;

        async function interactionChange(past_card) {
            //console.log(past_card);
            const response = await fetch(`/api-v2/change/flashcard-interaction/?page=${past_card["notepage_id"]}&flashcards=${past_card["block_id"]}&flashcard=${past_card["id"]}&score=${correct}`);
            return await response.json()
        }


        interactionChange(past_card).then(json => {
            //console.log(json);
            this.card_holder.update_card(json);
        })


        document.getElementById("quiz-score-" + id_end).innerHTML = this.amountCorrect();

        document.getElementById("quiz-btn-" + id_end).style.display = "initial";

        document.getElementById("quiz-q-" + id_end).innerHTML = card["q"];


        if (card && (!this.cardsSeen.includes(card["id"]))) {
            this.current_index_unique += 1;
            this.cardsSeen.push(card["id"])

        }
        document.getElementById("quiz-progress-" + id_end).innerHTML = `${this.current_index + 1} | ${this.current_index_unique + 1}`;


        return false
    }

    begin() {
        this.scores = {};
        this.current_index_unique = 0;
        this.current_index = 0;
    }

    amountCorrect() {
        let summed = 0;
        for (const elem of Object.values(this.scores)) {
            if (!(elem === undefined)) {
                summed += elem;

            }
        }
        return Math.round(summed)
    }

    quizRunner() {
        if (this.current_index === 0) {
            this.begin();
            document.getElementById("quiz-btn-nextspan-" + id_end).style.display = "inline";
            document.getElementById("quiz-btn-restartspan-" + id_end).style.display = "none";
        }

        let card = this.card_holder.past_card;

        toggleShow("quiz-btn-next-" + id_end);
        document.getElementById("quiz-btn-" + id_end).style.display = "none";
        document.getElementById("quiz-q-" + id_end).innerHTML = card["q"] + "<hr>" + card["a"];

        this.current_index += 1;

        return false
    }
}