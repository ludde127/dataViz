"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) {
        return value instanceof P ? value : new P(function (resolve) {
            resolve(value);
        });
    }

    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) {
            try {
                step(generator.next(value));
            } catch (e) {
                reject(e);
            }
        }

        function rejected(value) {
            try {
                step(generator["throw"](value));
            } catch (e) {
                reject(e);
            }
        }

        function step(result) {
            result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected);
        }

        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __classPrivateFieldGet = (this && this.__classPrivateFieldGet) || function (receiver, state, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state.get(receiver);
};
var _Deck_instances, _Deck_heuristic, _Deck_sort, _Deck_dump, _YapityFlashcards_instances, _YapityFlashcards_flip,
    _YapityFlashcards_showCard, _YapityFlashcards_nextCard, _YapityFlashcards_cardInteraction;

class Deck {
    constructor(cards) {
        _Deck_instances.add(this);
        this.cards = cards;
        __classPrivateFieldGet(this, _Deck_instances, "m", _Deck_sort).call(this);
    }

    draw() {
        return this.cards.shift();
    }

    insert(card) {
        this.cards.push(card);
        __classPrivateFieldGet(this, _Deck_instances, "m", _Deck_sort).call(this);
    }

    score() {
        let sum = 0;
        for (const card of this.cards) {
            if (card.lastScore)
                sum += card.lastScore;
        }
        return sum;
    }
}

_Deck_instances = new WeakSet(), _Deck_heuristic = function _Deck_heuristic(card) {
    const secondsSinceLastDisplayed = Date.now() / 1000.0 - card.last_displayed_float;
    const decay = 150 * Math.exp(-secondsSinceLastDisplayed / 60.0);
    return card.weight - decay;
}, _Deck_sort = function _Deck_sort() {
    this.cards.sort((a, b) => __classPrivateFieldGet(this, _Deck_instances, "m", _Deck_heuristic).call(this, b) - __classPrivateFieldGet(this, _Deck_instances, "m", _Deck_heuristic).call(this, a));
}, _Deck_dump = function _Deck_dump() {
    this.cards.map(c => `${__classPrivateFieldGet(this, _Deck_instances, "m", _Deck_heuristic).call(this, c)}: ${Date.now() / 1000.0 - c.last_displayed_float}: ${c.weight}: ${c.q.slice(0, 40)}...`).forEach(c => console.log(c));
    console.log(this.cards);
};

class YapityFlashcards extends HTMLElement {
    constructor() {
        var _a;
        super();
        _YapityFlashcards_instances.add(this);
        this.flashcards = JSON.parse(this.dataset.cards);
        this.deck = new Deck(this.flashcards);
        this.cardNumber = 1;
        this.progressBadge = this.querySelector("#progress-badge");
        this.scoreBadge = this.querySelector("#score-badge");
        this.interactionButtons = this.querySelectorAll("[data-score]");
        this.interactionButtons.forEach(e => e.addEventListener("click", () => __classPrivateFieldGet(this, _YapityFlashcards_instances, "m", _YapityFlashcards_nextCard).call(this, parseFloat(e.dataset.score))));
        (_a = this.querySelector("#face-container")) === null || _a === void 0 ? void 0 : _a.addEventListener("click", () => __classPrivateFieldGet(this, _YapityFlashcards_instances, "m", _YapityFlashcards_flip).call(this));
        this.frontFace = this.querySelector("#front-face");
        this.frontFaceContent = this.frontFace.querySelector("#face-content");
        this.backFace = this.querySelector("#back-face");
        this.backFaceContent = this.backFace.querySelector("#face-content");
        this.currentCard = this.deck.draw();
        this.faceUp = "front";
        __classPrivateFieldGet(this, _YapityFlashcards_instances, "m", _YapityFlashcards_showCard).call(this);
    }
}

_YapityFlashcards_instances = new WeakSet(), _YapityFlashcards_flip = function _YapityFlashcards_flip() {
    this.frontFace.classList.toggle("flashcard-flip-in");
    this.frontFace.classList.toggle("flashcard-flip-out");
    this.backFace.classList.toggle("flashcard-flip-in");
    this.backFace.classList.toggle("flashcard-flip-out");
    this.interactionButtons.forEach(e => e.classList.toggle("btn-disabled"));
    this.faceUp = this.faceUp == "front" ? "back" : "front";
    __classPrivateFieldGet(this, _YapityFlashcards_instances, "m", _YapityFlashcards_showCard).call(this);
}, _YapityFlashcards_showCard = function _YapityFlashcards_showCard() {
    if (this.faceUp == "front") {
        this.frontFaceContent.innerHTML = this.currentCard.q;
    } else {
        this.backFaceContent.innerHTML = this.currentCard.a;
    }
}, _YapityFlashcards_nextCard = function _YapityFlashcards_nextCard(score) {
    return __awaiter(this, void 0, void 0, function* () {
        const updates = yield __classPrivateFieldGet(this, _YapityFlashcards_instances, "m", _YapityFlashcards_cardInteraction).call(this, this.currentCard, score);
        const newCard = Object.assign(Object.assign(Object.assign({}, this.currentCard), updates), {lastScore: score});
        this.deck.insert(newCard);
        this.scoreBadge.textContent = this.deck.score().toFixed(1);
        this.currentCard = this.deck.draw();
        this.progressBadge.textContent = (++this.cardNumber).toString();
        __classPrivateFieldGet(this, _YapityFlashcards_instances, "m", _YapityFlashcards_flip).call(this);
    });
}, _YapityFlashcards_cardInteraction = function _YapityFlashcards_cardInteraction(card, score) {
    return __awaiter(this, void 0, void 0, function* () {
        const response = yield fetch("/api-v2/change/flashcard-interaction/", {
            method: "POST",
            body: JSON.stringify({
                page: card.notepage_id,
                flashcards: card.block_id,
                flashcard: card.id,
                score,
            })
        });
        return yield response.json();
    });
};
customElements.define("yapity-flashcards", YapityFlashcards);
//# sourceMappingURL=flashcards.js.map