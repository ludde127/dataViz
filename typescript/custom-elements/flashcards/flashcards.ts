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
    scores: Array<number>;

    scoreBadge: HTMLElement;
    flipButton: HTMLElement;
    interactionButtons: NodeListOf<Element>;

    frontFace: HTMLElement;
    frontFaceContent: HTMLElement;
    backFace: HTMLElement;
    backFaceContent: HTMLElement;

    currentCard: Flashcard;

    faceUp: "front" | "back";

    constructor() {
        super();

        this.flashcards = JSON.parse(this.dataset.cards!);
        this.deck = new Deck(this.flashcards);
        this.scores = [];

        this.scoreBadge = this.querySelector("#score-badge")!;

        this.flipButton = this.querySelector("#flip-button")!;
        this.flipButton?.addEventListener("click", () => this.#flip());

        // Add event listeners to progression buttons
        this.interactionButtons = this.querySelectorAll("[data-score]");
        this.interactionButtons.forEach(e =>
            e.addEventListener("click", () => this.#nextCard(parseFloat((e as HTMLElement).dataset.score!)))
        );

        this.querySelector("#face-container")?.addEventListener("click", () => this.#flip());
        this.frontFace = this.querySelector("#front-face")!;
        this.frontFaceContent = this.frontFace.querySelector("#face-content")!;
        this.backFace = this.querySelector("#back-face")!;
        this.backFaceContent = this.backFace.querySelector("#face-content")!;

        this.currentCard = this.deck.draw();

        this.faceUp = "front";
        this.#showCard();
    }


    #flip() {
        this.frontFace.classList.toggle("flashcard-flip-in");
        this.frontFace.classList.toggle("flashcard-flip-out");
        this.backFace.classList.toggle("flashcard-flip-in");
        this.backFace.classList.toggle("flashcard-flip-out");
        this.flipButton.classList.add("hidden");
        this.interactionButtons.forEach(e => {
            console.log("toggle");
            e.classList.toggle("btn-disabled")
        });
        this.faceUp = this.faceUp == "front" ? "back" : "front";
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
        const updates = await this.#cardInteraction(this.currentCard, score);
        const newCard: Flashcard = {...this.currentCard, ...updates};
        this.deck.insert(newCard);
        this.currentCard = this.deck.draw();
        this.#flip();
        this.#showCard();
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
}

customElements.define("yapity-flashcards", YapityFlashcards);
