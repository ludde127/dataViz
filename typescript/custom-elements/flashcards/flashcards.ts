type Flashcard = {
    q: string;
    a: string;
    block_id: string;
    id: string;
    last_displayed_float: number;
    notepage_id: number;
    score: number;
    times_displayed: number;
    weight: number;
    lastScore?: number;
};
type InteractionResponse = Pick<Flashcard, "id" | "score" | "times_displayed" | "weight" | "last_displayed_float">;

class Deck {
    cards: Array<Flashcard>;

    constructor(cards: Array<Flashcard>) {
        this.cards = cards;
        this.#sort();
    }

    draw() {
        return this.cards.shift()!;
    }

    insert(card: Flashcard) {
        this.cards.push(card);
        this.#sort();
    }

    score() {
        let sum = 0;
        for (const card of this.cards) {
            if (card.lastScore) sum += card.lastScore;
        }
        return sum;
    }

    #heuristic(card: Flashcard) {
        const secondsSinceLastDisplayed = Date.now() / 1000.0 - card.last_displayed_float;
        const decay = 150 * Math.exp(-secondsSinceLastDisplayed / 60.0);
        return card.weight - decay;
    }

    #sort() {
        this.cards.sort((a, b) => this.#heuristic(b) - this.#heuristic(a));
    }

    #dump() {
        this.cards.map(c => `${this.#heuristic(c)}: ${Date.now() / 1000.0 - c.last_displayed_float}: ${c.weight}: ${c.q.slice(0, 40)}...`).forEach(c => console.log(c));
        console.log(this.cards);
    }

}

class YapityFlashcards extends HTMLElement {
    flashcards: Array<Flashcard>;
    deck: Deck;

    progressBadge: HTMLElement;
    scoreBadge: HTMLElement;

    interactionButtons: NodeListOf<Element>;

    frontFace: HTMLElement;
    frontFaceContent: HTMLElement;
    backFace: HTMLElement;
    backFaceContent: HTMLElement;

    currentCard: Flashcard;

    faceUp: "front" | "back";
    cardNumber: number;

    constructor() {
        super();

        // Setup data
        this.flashcards = JSON.parse(this.dataset.cards!);
        this.deck = new Deck(this.flashcards);

        this.cardNumber = 1;
        this.progressBadge = this.querySelector("#progress-badge")!;
        this.scoreBadge = this.querySelector("#score-badge")!;

        // Add event listeners to progression buttons
        this.interactionButtons = this.querySelectorAll("[data-score]");
        this.interactionButtons.forEach(e =>
            e.addEventListener("click", () => this.#nextCard(parseFloat((e as HTMLElement).dataset.score!)))
        );

        // Setup faces
        this.querySelector("#face-container")?.addEventListener("click", () => this.#flip());
        this.frontFace = this.querySelector("#front-face")!;
        this.frontFaceContent = this.frontFace.querySelector("#face-content")!;
        this.backFace = this.querySelector("#back-face")!;
        this.backFaceContent = this.backFace.querySelector("#face-content")!;

        // Setup first card
        this.currentCard = this.deck.draw();
        this.faceUp = "front";
        this.#showCard();
    }


    #flip() {
        this.faceUp = this.faceUp == "front" ? "back" : "front";

        this.frontFace.classList.toggle("flashcard-flip-in");
        this.frontFace.classList.toggle("flashcard-flip-out");
        this.backFace.classList.toggle("flashcard-flip-in");
        this.backFace.classList.toggle("flashcard-flip-out");

        this.interactionButtons.forEach(e => {
            if (this.faceUp == "front") {
                this.#disableButtons();
            } else {
                this.#enableButtons();
            }
        });

        this.#showCard();
    }

    #showCard() {
        if (this.faceUp == "front") {
            this.frontFaceContent.innerHTML = this.currentCard.q;
        } else {
            this.backFaceContent.innerHTML = this.currentCard.a;
        }
    }

    async #nextCard(score: number) {
        this.#disableButtons();

        const updates = await this.#cardInteraction(this.currentCard, score);
        const newCard: Flashcard = {...this.currentCard, ...updates, lastScore: score};

        this.deck.insert(newCard);
        this.scoreBadge.textContent = this.deck.score().toFixed(1);
        this.currentCard = this.deck.draw();

        this.progressBadge.textContent = (++this.cardNumber).toString();

        this.#flip();
    }

    async #cardInteraction(card: Flashcard, score: number) {
        const response = await fetch("/api-v2/change/flashcard-interaction/", {
            method: "POST",
            body: JSON.stringify({
                page: card.notepage_id,
                flashcards: card.block_id,
                flashcard: card.id,
                score,
            })
        });
        return await response.json() as InteractionResponse;
    }

    #disableButtons() {
        this.interactionButtons.forEach(e => e.classList.add("btn-disabled"));
    }

    #enableButtons() {
        this.interactionButtons.forEach(e => e.classList.remove("btn-disabled"));
    }
}

customElements.define("yapity-flashcards", YapityFlashcards);
