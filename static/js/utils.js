export default function toggleShow(elementId) {
    const element = document.getElementById(elementId);
    element?.classList.toggle("hidden");
}