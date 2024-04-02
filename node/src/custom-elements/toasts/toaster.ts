class YapityToaster extends HTMLElement {
    constructor() {
        super();

        const toasts = [...this.querySelectorAll(".alert")] as Array<HTMLElement>;

        toasts.forEach(e => {
            const startTimeout = () => setTimeout(
                () => e.classList.add("toast-fly-out"),
                10000);
            let timeout = startTimeout();
            e.addEventListener("mouseover", () => {
                console.log("mouseover");
                clearTimeout(timeout)
            });
            e.addEventListener("mouseleave", () => {
                console.log("mouseleave");
                timeout = startTimeout()
            });
        });
    }
}

customElements.define("yapity-toaster", YapityToaster);