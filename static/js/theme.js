const setTheme = (theme, colorScheme) => {
    const root = document.querySelector(":root");
    root.dataset.theme = theme;
    root.style.colorScheme = colorScheme;
    localStorage.setItem("theme", theme);
    localStorage.setItem("colorScheme", colorScheme);
};
const checkTheme = () => {
    if (localStorage.theme) {
        setTheme(localStorage.theme, localStorage.colorScheme);
    } else if ((!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        setTheme("dark", "dark");
    } else {
        setTheme("light", "light");
    }
};
// Immediately check the theme on page load
checkTheme();

// Add event listeners to the theme picker in the navbar
window.addEventListener("load", () => {
    for (const element of document.getElementsByName("theme-dropdown")) {
        element.addEventListener(
            "click",
            _ => setTheme(
                element.dataset.setTheme,
                element.dataset.hasOwnProperty("dark") ? "dark" : "light"));
    }
});
// Add event listener to the local storage so that all tabs sync their theme with each other
window.addEventListener("storage", function (e) {
    checkTheme();
}, false);
