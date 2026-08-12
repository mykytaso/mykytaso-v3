// Toggle between light and dark themes.
// - If the checkbox is checked → set theme to "dark"
// - Otherwise → set theme to "light"
// - Apply the theme by setting the <html> attribute: <html theme="...">
// - Save the selected theme in localStorage so it persists on reload
// - Update theme-color meta tag for mobile browser UI
function toggleTheme(checkbox) {
    const theme = checkbox.checked ? "dark" : "light";
    document.documentElement.setAttribute("theme", theme);
    localStorage.setItem("theme", theme);

    // Update theme-color meta tag for mobile browser UI
    const metaThemeColor = document.querySelector('meta[name="theme-color"]:not([media])') ||
                           document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.setAttribute('content', theme === 'dark' ? '#0C1014' : '#ffffff');
    }
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

// Editor image panel: copy the URL of an image to the clipboard.
function handleImagePanelClick(event) {
    const copyButton = event.target.closest("[data-copy-url]");
    if (!copyButton) {
        return;
    }

    navigator.clipboard.writeText(copyButton.dataset.copyUrl).then(() => {
        const original = copyButton.textContent;
        copyButton.textContent = "Copied";
        setTimeout(() => { copyButton.textContent = original; }, 1200);
    });
}

// Close mobile menu when clicking outside
function closeMobileMenuOnOutsideClick(event) {
    const menu = document.getElementById('navbar-menu');
    const burgerIcon = event.target.closest('.show-on-iphone');

    // Only proceed if menu exists and is visible
    if (!menu || !menu.classList.contains('navbar__menu--visible')) {
        return;
    }

    // Don't close if clicking on the burger icon or menu itself
    if (burgerIcon || menu.contains(event.target)) {
        return;
    }

    // Close the menu
    menu.classList.remove('navbar__menu--visible');
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

    // Initialize image zoom for post images
    initializeImageZoom();

    // Add click listener to close mobile menu when clicking outside
    document.addEventListener('click', closeMobileMenuOnOutsideClick);

    // Editor image panel buttons (superuser only pages)
    document.addEventListener('click', handleImagePanelClick);
});
