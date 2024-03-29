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
var _YapityFlashcardsSubscribeButton_instances, _YapityFlashcardsSubscribeButton_toggleSubscription;

class YapityFlashcardsSubscribeButton extends HTMLElement {
    constructor() {
        super();
        _YapityFlashcardsSubscribeButton_instances.add(this);
        this.blockId = this.dataset.blockId;
        this.pageId = this.dataset.pageId;
        this.isSubscribed = this.dataset.isSubscribed !== undefined;
        this.button = this.querySelector("button");
        this.button.addEventListener("click", _ => __classPrivateFieldGet(this, _YapityFlashcardsSubscribeButton_instances, "m", _YapityFlashcardsSubscribeButton_toggleSubscription).call(this));
    }
}

_YapityFlashcardsSubscribeButton_instances = new WeakSet(), _YapityFlashcardsSubscribeButton_toggleSubscription = function _YapityFlashcardsSubscribeButton_toggleSubscription() {
    return __awaiter(this, void 0, void 0, function* () {
        this.button.classList.add("btn-disabled");
        this.button.textContent = "Loading";
        const res = yield fetch(`/api-v2/change/${this.isSubscribed ? "unsubscribe" : "subscribe"}/`, {
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
    });
};
customElements.define("yapity-flashcards-subscribe-button", YapityFlashcardsSubscribeButton);
//# sourceMappingURL=subscribe-button.js.map