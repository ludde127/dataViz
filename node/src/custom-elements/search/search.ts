import DOMPurify from "dompurify";
import {createElement, FileText, IconNode, LineChart, Tag, UserRound} from "lucide";

type SearchResult = {
    name: string;
    url: string;
    type: "page" | "datastore" | "user" | "tag"
};
type SearchResults = Record<string, Array<SearchResult>>;

const getIcon = (icon: IconNode) => {
    const i = createElement(icon);
    i.classList.add("w-4", "h-4");
    return i;
}

const ICON_TEMPLATES = {
    page: getIcon(FileText),
    datastore: getIcon(LineChart),
    user: getIcon(UserRound),
    tag: getIcon(Tag),
}

class YapitySearch extends HTMLElement {
    searchButton: HTMLButtonElement;
    searchModal: HTMLDialogElement;
    searchInput: HTMLInputElement;
    searchResultsContainer: HTMLElement;
    noSearchResultsContainer: HTMLElement;

    searchIcon: HTMLElement;
    loadingIcon: HTMLElement;

    abortController?: AbortController;
    iconTimeout?: number;
    focusIndex?: number;

    focusableElements: Array<HTMLAnchorElement>;

    constructor() {
        super();

        this.searchButton = this.querySelector("#search-button")!;
        this.searchModal = this.querySelector("#search-modal")!;
        this.searchInput = this.querySelector("#search-input")!;
        this.searchResultsContainer = this.querySelector("#search-results")!;
        this.noSearchResultsContainer = this.querySelector("#no-search-results")!;

        this.searchIcon = this.querySelector("#search-icon")!;
        this.loadingIcon = this.querySelector("#loading-icon")!;

        this.searchButton.addEventListener("click", () => {
            this.#openModal();
        });
        document.addEventListener("keydown", e => {
            if (e.key === "k" && e.ctrlKey) {
                e.preventDefault();

                if (!this.searchModal.open) {
                    this.searchInput.value = "";
                }

                this.#openModal();
            }
            if (this.searchModal.open) {
                if (e.target === this.searchInput && this.focusIndex !== undefined) {
                    let delta = 0;
                    switch (e.key) {
                        case "ArrowUp":
                            delta = -1;
                            break;
                        case "ArrowDown":
                            delta = 1;
                            break;
                        case "Enter":
                            this.#selectFocusedResult();
                            break;
                    }
                    if (delta !== 0) {
                        e.preventDefault();
                        const n = this.focusableElements.length;
                        this.#updateFocus((this.focusIndex + n + delta) % n, true);
                    }
                }
            }
        });

        this.focusableElements = [];

        this.searchInput.addEventListener("input", e => {
            this.#search(this.searchInput.value);
        });
    }

    #openModal() {
        this.searchModal.showModal();
    }

    async #search(query: string) {
        try {
            this.#setLoadingState(true);
            const searchResults = await this.#getSearchResults(query);
            this.#setLoadingState(false);

            this.#updateSearchResults(searchResults);
        } catch (e) {
            console.log(e);
        }
    }

    async #getSearchResults(query: string) {
        if (this.abortController) {
            this.abortController.abort();
        }

        this.abortController = new AbortController();
        const res = await fetch('/search/?' + new URLSearchParams({
            query
        }), {
            method: "GET",
            signal: this.abortController.signal
        });

        if (!res.ok) {
            return {}
        }

        return await res.json() as SearchResults;
    }

    #setLoadingState(isLoading: boolean) {
        clearTimeout(this.iconTimeout);
        this.iconTimeout = setTimeout(() => {
            this.loadingIcon.classList.toggle("hidden", !isLoading);
            this.searchIcon.classList.toggle("hidden", isLoading);
        }, isLoading ? 0 : 150);
    }

    #updateSearchResults(searchResults: SearchResults) {
        const children = [];
        for (const type in searchResults) {
            if (searchResults[type].length <= 0) continue;

            const div = document.createElement("div");
            div.classList.add("menu");

            // Add type header
            div.innerHTML += `<li class="opacity-60 pb-2">${type}</li>`

            // Add search results for the specific type
            div.innerHTML += searchResults[type].map(
                sr => `<li>
                    <a href="${sr.url}" class="">
                        ${ICON_TEMPLATES[sr.type]?.outerHTML || ""}${DOMPurify.sanitize(sr.name, {USE_PROFILES: {html: true}})}
                    </a>
                </li>`).join("");

            children.push(div);
        }
        const hasResults = children.length > 0;

        this.searchResultsContainer.replaceChildren(...children);

        this.focusableElements = [...this.searchResultsContainer.querySelectorAll("a")];
        this.focusableElements.forEach((e, i) => {
            e.addEventListener("mouseenter", () => {
                this.#updateFocus(i, false);
            });
        })

        this.searchResultsContainer.classList.toggle("hidden", !hasResults);
        this.noSearchResultsContainer.classList.toggle("hidden", hasResults);

        this.#updateFocus(hasResults ? 0 : undefined, true);
    }

    #updateFocus(index?: number, scroll?: boolean) {
        if (this.focusIndex !== undefined) {
            this.focusableElements[this.focusIndex]?.classList.remove("focus");
        }

        this.focusIndex = index;

        if (this.focusIndex !== undefined) {
            const element = this.focusableElements[this.focusIndex];
            element.classList.add("focus");
            if (scroll) {
                element.scrollIntoView({block: "center", behavior: "smooth"});
            }
        }
    }

    #selectFocusedResult() {
        if (this.focusIndex !== undefined) {
            const a = this.focusableElements[this.focusIndex];
            document.location.href = a.href;
        }
    }
}

customElements.define("yapity-search", YapitySearch);