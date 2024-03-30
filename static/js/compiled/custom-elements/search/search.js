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
var _YapitySearch_instances, _YapitySearch_openModal, _YapitySearch_search, _YapitySearch_getSearchResults,
    _YapitySearch_setLoadingState, _YapitySearch_updateSearchResults, _YapitySearch_updateFocus,
    _YapitySearch_selectFocusedResult;

class YapitySearch extends HTMLElement {
    constructor() {
        super();
        _YapitySearch_instances.add(this);
        this.searchButton = this.querySelector("#search-button");
        this.searchModal = this.querySelector("#search-modal");
        this.searchInput = this.querySelector("#search-input");
        this.searchResultsContainer = this.querySelector("#search-results");
        this.noSearchResultsContainer = this.querySelector("#no-search-results");
        this.iconTemplates = {
            page: this.querySelector("#icon-template-page"),
            datastore: this.querySelector("#icon-template-datastore"),
        };
        this.searchIcon = this.querySelector("#search-icon");
        this.loadingIcon = this.querySelector("#loading-icon");
        this.searchButton.addEventListener("click", () => {
            __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_openModal).call(this);
        });
        document.addEventListener("keydown", e => {
            if (e.key === "k" && e.ctrlKey) {
                e.preventDefault();
                __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_openModal).call(this);
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
                        __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_selectFocusedResult).call(this);
                        break;
                }
                if (delta !== 0) {
                    e.preventDefault();
                    const n = this.searchResultsContainer.children.length;
                    __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_updateFocus).call(this, (this.focusIndex + n + delta) % n);
                }
            }
        });
        let first = Date.now();
        this.searchInput.addEventListener("input", e => {
            first = Date.now();
            __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_search).call(this, this.searchInput.value);
        });
    }
}

_YapitySearch_instances = new WeakSet(), _YapitySearch_openModal = function _YapitySearch_openModal() {
    this.searchModal.showModal();
}, _YapitySearch_search = function _YapitySearch_search(query) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_setLoadingState).call(this, true);
            const searchResults = yield __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_getSearchResults).call(this, query);
            __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_setLoadingState).call(this, false);
            __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_updateSearchResults).call(this, searchResults);
        } catch (e) {
            console.log(e);
        }
    });
}, _YapitySearch_getSearchResults = function _YapitySearch_getSearchResults(query) {
    return __awaiter(this, void 0, void 0, function* () {
        if (this.abortController) {
            this.abortController.abort();
        }
        this.abortController = new AbortController();
        const res = yield fetch('/search/?' + new URLSearchParams({
            query
        }), {
            method: "GET",
            signal: this.abortController.signal
        });
        return yield res.json();
    });
}, _YapitySearch_setLoadingState = function _YapitySearch_setLoadingState(isLoading) {
    clearTimeout(this.iconTimeout);
    this.iconTimeout = setTimeout(() => {
        this.loadingIcon.classList.toggle("hidden", !isLoading);
        this.searchIcon.classList.toggle("hidden", isLoading);
    }, isLoading ? 0 : 150);
}, _YapitySearch_updateSearchResults = function _YapitySearch_updateSearchResults(searchResults) {
    const hasResults = searchResults.results.length > 0;
    this.searchResultsContainer.replaceChildren(...searchResults.results.map(sr => {
        const template = document.createElement("template");
        template.innerHTML = `<li>
                        <a href="${sr.url}">
                            ${this.iconTemplates[sr.type].outerHTML}${sr.name}
                        </a>
                    </li>`;
        return template.content.children[0];
    }));
    this.searchResultsContainer.classList.toggle("hidden", !hasResults);
    this.noSearchResultsContainer.classList.toggle("hidden", hasResults);
    __classPrivateFieldGet(this, _YapitySearch_instances, "m", _YapitySearch_updateFocus).call(this, hasResults ? 0 : undefined);
}, _YapitySearch_updateFocus = function _YapitySearch_updateFocus(index) {
    var _a, _b;
    if (this.focusIndex !== undefined) {
        (_a = this.searchResultsContainer
            .children[this.focusIndex]
            .children[0]) === null || _a === void 0 ? void 0 : _a.classList.remove("focus");
    }
    this.focusIndex = index;
    if (this.focusIndex !== undefined) {
        console.log("here");
        (_b = this.searchResultsContainer
            .children[this.focusIndex]
            .children[0]) === null || _b === void 0 ? void 0 : _b.classList.add("focus");
    }
}, _YapitySearch_selectFocusedResult = function _YapitySearch_selectFocusedResult() {
    if (this.focusIndex !== undefined) {
        const a = this.searchResultsContainer.children[this.focusIndex].children[0];
        document.location.replace(a.href);
    }
};
customElements.define("yapity-search", YapitySearch);
//# sourceMappingURL=search.js.map