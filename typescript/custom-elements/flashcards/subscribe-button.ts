class YapityFlashcardsSubscribeButton extends HTMLElement {
    blockId: string;
    pageId: string;
    isSubscribed: boolean;

    button: HTMLElement;

    constructor() {
        super();

        this.blockId = this.dataset.blockId!;
        this.pageId = this.dataset.pageId!;
        this.isSubscribed = this.dataset.isSubscribed !== undefined;

        this.button = this.querySelector("button")!;
        this.button.addEventListener("click", _ => this.#toggleSubscription());
    }

    async #toggleSubscription() {
        this.button.classList.add("btn-disabled");
        this.button.textContent = "Loading";

        const res = await fetch(`/api-v2/change/${this.isSubscribed ? "unsubscribe" : "subscribe"}/`,
            {
                method: "POST",
                body: JSON.stringify({
                    page: this.pageId,
                    flashcards: this.blockId,
                })
            });

        if (res.ok) {
            this.isSubscribed = !this.isSubscribed;
        }

        this.button.classList.remove("btn-disabled");
        this.button.textContent = this.isSubscribed ? "Unsubscribe" : "Subscribe";
    }
}

customElements.define("yapity-flashcards-subscribe-button", YapityFlashcardsSubscribeButton);
