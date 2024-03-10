const setTheme = (theme) => {
    const root = document.querySelector(":root");
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    localStorage.setItem("theme", theme);
};

const checkTheme = () => {
    if (localStorage.theme) {
        setTheme(localStorage.theme);
    } else if ((!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        setTheme("dark");
    } else {
        setTheme("light");
    }
};

for (const element of document.getElementsByName("theme-dropdown")) {
    element.addEventListener("click", _ => setTheme(element.dataset.setTheme));
}

window.addEventListener("storage", function (e) {
    checkTheme();
}, false);

checkTheme();