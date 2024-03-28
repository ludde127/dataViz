type Flashcard = {
    q: string;
    a: string;
    block_id: string;
    id: string;
    last_display_float: number;
    notepage_id: number;
    score: number;
    times_displayed: number;
    weight: number;
};

class Deck {
    constructor(cards: Array<Flashcard>) {
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

        this.currentCard = this.flashcards[0];
        this.#showCard(this.currentCard);
    }


    #flip() {
        this.frontFace.classList.toggle("flashcard-flip-in");
        this.frontFace.classList.toggle("flashcard-flip-out");
        this.backFace.classList.toggle("flashcard-flip-in");
        this.backFace.classList.toggle("flashcard-flip-out");
        this.flipButton.classList.add("hidden");
        this.interactionButtons.forEach(e => e.classList.toggle("btn-disabled"));
    }

    #showCard(card: Flashcard) {
        this.frontFaceContent.innerHTML = card.q;
        this.backFaceContent.innerHTML = card.a;
    }

    #nextCard(score: number) {
        console.log(`next card ${score}`)
        console.log(this.#cardInteraction(this.currentCard, score));
    }

    async #cardInteraction(card: Flashcard, score: number) {
        const response = await fetch("/api-v2/change/flashcard-interaction/", {
            method: "POST",
            body: JSON.stringify({
                page: card.notepage_id,
                flashcards: card.block_id,
                flashcard: card.id,
                score
            })
        });
        const data = await response.json();
        return JSON.parse(data) as Flashcard;
    }
}

customElements.define("yapity-flashcards", YapityFlashcards);
