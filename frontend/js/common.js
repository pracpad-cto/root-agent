/**
 * Learning Portal - Common Utilities
 * 
 * This module provides shared UI utilities used across different pages
 * of the learning platform to maintain consistent behavior and appearance.
 * 
 * @author Abhijit Raijada
 * @designation Principle Engineer
 * @organization GRS
 */

/**
 * Common utility functions for the Learning Portal
 * This module provides shared UI utilities used across different pages
 * of the learning platform to maintain consistent behavior and appearance.
 */

/**
 * Create a typing loader animation element
 * Used to indicate when the AI is generating a response in chat interfaces
 * Shows three animated dots to simulate typing activity
 * 
 * @returns {HTMLElement} The loader element that can be appended to the DOM
 */
function createTypingLoader() {
    const loader = document.createElement('div');
    loader.className = 'typing-loader';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        loader.appendChild(dot);
    }
    return loader;
}

/**
 * Scroll a container to the bottom
 * Used to keep chat and conversation views scrolled to the most recent message
 * Particularly important during streaming responses to maintain visibility
 * 
 * @param {HTMLElement} container - The container element to scroll (typically a chat window)
 */
function scrollToBottom(container) {
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

/**
 * Create a back link element
 * Generates a consistent navigation link with back arrow for returning to previous screens
 * Used throughout the application to provide uniform navigation experience
 * 
 * @param {string} href - The link destination URL
 * @param {string} text - The link text to display
 * @returns {HTMLElement} The formatted link element ready to be inserted into the DOM
 */
function createBackLink(href, text) {
    const link = document.createElement('a');
    link.href = href;
    link.className = 'text-blue-500 hover:text-blue-700 mb-4 inline-block';
    link.innerHTML = `&larr; ${text}`;
    return link;
}

/**
 * Show an error message to the user
 * Displays a temporary notification for error conditions
 * Automatically removes itself after 5 seconds to avoid cluttering the UI
 * 
 * @param {string} message - The error message to display
 */
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4';
    errorDiv.role = 'alert';
    errorDiv.innerHTML = `
        <strong class="font-bold">Error!</strong>
        <span class="block sm:inline">${message}</span>
    `;
    
    // Add to page at the top of the container
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(errorDiv, container.firstChild);
    
    // Remove after 5 seconds to avoid cluttering the interface
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Make utility functions globally available for use in other modules
window.createTypingLoader = createTypingLoader;
window.scrollToBottom = scrollToBottom;
window.createBackLink = createBackLink;
window.showError = showError;
