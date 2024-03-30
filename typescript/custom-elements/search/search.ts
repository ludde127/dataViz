type SearchResult = {
    name: string;
    url: string;
    type: "page" | "datastore"
};
type SearchResults = {
    results: Array<SearchResult>;
};

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

    iconTemplates: Record<SearchResult['type'], HTMLElement>;

    constructor() {
        super();

        this.searchButton = this.querySelector("#search-button")!;
        this.searchModal = this.querySelector("#search-modal")!;
        this.searchInput = this.querySelector("#search-input")!;
        this.searchResultsContainer = this.querySelector("#search-results")!;
        this.noSearchResultsContainer = this.querySelector("#no-search-results")!;

        this.iconTemplates = {
            page: this.querySelector("#icon-template-page")!,
            datastore: this.querySelector("#icon-template-datastore")!,
        }

        this.searchIcon = this.querySelector("#search-icon")!;
        this.loadingIcon = this.querySelector("#loading-icon")!;

        this.searchButton.addEventListener("click", () => {
            this.#openModal();
        });
        document.addEventListener("keydown", e => {
            if (e.key === "k" && e.ctrlKey) {
                e.preventDefault();
                this.#openModal();
            }
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
                    const n = this.searchResultsContainer.children.length;
                    this.#updateFocus((this.focusIndex + n + delta) % n);
                }
            }
        });

        let first = Date.now();
        this.searchInput.addEventListener("input", e => {
            first = Date.now();
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
        const hasResults = searchResults.results.length > 0;

        this.searchResultsContainer.replaceChildren(
            ...searchResults.results.map(
                sr => {
                    const template = document.createElement("template");
                    template.innerHTML = `<li>
                        <a href="${sr.url}">
                            ${this.iconTemplates[sr.type].outerHTML}${sr.name}
                        </a>
                    </li>`;
                    return template.content.children[0];
                }
            ));

        this.searchResultsContainer.classList.toggle("hidden", !hasResults);
        this.noSearchResultsContainer.classList.toggle("hidden", hasResults);

        this.#updateFocus(hasResults ? 0 : undefined);
    }

    #updateFocus(index?: number) {
        if (this.focusIndex !== undefined) {
            this.searchResultsContainer
                .children[this.focusIndex]
                .children[0]
                ?.classList.remove("focus");
        }

        this.focusIndex = index;

        if (this.focusIndex !== undefined) {
            console.log("here");
            this.searchResultsContainer
                .children[this.focusIndex]
                .children[0]
                ?.classList.add("focus");
        }
    }

    #selectFocusedResult() {
        if (this.focusIndex !== undefined) {
            const a = this.searchResultsContainer.children[this.focusIndex].children[0] as HTMLAnchorElement;
            document.location.replace(a.href);
        }
    }
}

customElements.define("yapity-search", YapitySearch);