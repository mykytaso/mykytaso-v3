// Toggle between light and dark themes.
// - If the checkbox is checked → set theme to "dark"
// - Otherwise → set theme to "light"
// - Apply the theme by setting the <html> attribute: <html theme="...">
// - Save the selected theme in localStorage so it persists on reload
function toggleTheme(checkbox) {
    const theme = checkbox.checked ? "dark" : "light";
    document.documentElement.setAttribute("theme", theme);
    localStorage.setItem("theme", theme);
}

// Initialize theme switcher event listener when DOM is ready
document.addEventListener("DOMContentLoaded", function() {
    const themeCheckbox = document.getElementById("theme-checkbox");
    if (themeCheckbox) {
        // Attach change event listener to the checkbox
        themeCheckbox.addEventListener("change", function() {
            toggleTheme(this);
        });
    }
});
