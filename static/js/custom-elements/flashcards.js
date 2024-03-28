class YapityFlashcards extends HTMLElement {
    constructor() {
        super();

        this.cards = JSON.parse(this.dataset.cards);
        console.log(this.cards);
    }
}

customElements.define("yapity-flashcards", YapityFlashcards);