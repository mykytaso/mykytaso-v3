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

// Convert UTC timestamps to browser's local timezone
function convertTimestamps() {
    const timestamps = document.querySelectorAll('.comment-timestamp');

    timestamps.forEach(function(element) {
        const isoTimestamp = element.getAttribute('data-timestamp');
        if (!isoTimestamp) return;

        const date = new Date(isoTimestamp);

        // Format: "20.12.2025 19:33"
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');

        element.textContent = `${day}.${month}.${year}\u00A0\u00A0\u00A0${hours}:${minutes}`;
    });
}

function initializeImageZoom() {
    Lightense(document.querySelectorAll(".post__content img"), {
        time: 300,
        padding: 40,
        offset: 40,
        keyboard: true,
        cubicBezier: "cubic-bezier(.2, 0, .1, 1)",
        background: "var(--bg-color)",
        zIndex: 2147483647,
    });
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

    // Convert timestamps to local timezone
    convertTimestamps();

    // Initialize image zoom for post images
    initializeImageZoom();
});
