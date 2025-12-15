// Toggle between light and dark themes.
// - If the checkbox is checked → set theme to "dark"
// - Otherwise → set theme to "light"
// - Apply the theme by setting the <html> attribute: <html theme="...">
// - Save the selected theme in localStorage so it persists on reload
function toggleTheme(event) {
    let theme = event.target.checked ? "dark" : "light";
    document.documentElement.setAttribute("theme", theme);
    localStorage.setItem("theme", theme);
}
