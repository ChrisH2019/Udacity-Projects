/**
 * 
 * Manipulating the DOM exercise.
 * Exercise programmatically builds navigation,
 * scrolls to anchors from navigation,
 * and highlights section in viewport upon scrolling.
 * 
 * Dependencies: None
 * 
 * JS Version: ES2015/ES6
 * 
 * JS Standard: ESlint
 * 
*/

/**
 * Define Global Variables
 * 
*/
const navbar = document.getElementById("navbar__list");
const sections = document.querySelectorAll("section");

/**
 * End Global Variables
 * Start Helper Functions
 * 
*/
function isInViewport (element) {
    // Get element position within the viewport
    let distance = element.getBoundingClientRect();

    // Return true if element is in the viewport
    return (
        distance.top >= 0 &&
        distance.left >= 0 &&
        distance.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        distance.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}


/**
 * End Helper Functions
 * Begin Main Functions
 * 
*/

// build the nav
function buildNavebar() {
    // Create a container for new li element
    const navbarFragment = document.createDocumentFragment();

    for (let section of sections) {
        // Create li element
        const liElement = document.createElement('li');
        // Set class name
        liElement.className = 'menu__link';
        // Set data nav
        liElement.dataset.nav = section.id;
        // Set inner text
        liElement.innerText = section.dataset.nav;
        // Append li element to fragment
        navbarFragment.appendChild(liElement);
    }

    // Append navigation fragment to navigation bar
    navbar.appendChild(navbarFragment);
}


// Add class 'active' to section when near top of viewport
function setActive() {
    // Register scroll event listener in window
    window.addEventListener("scroll", function(event) {
        // Check which sectio is in viewport
        for (let section of sections) {
            if (isInViewport(section)) {
                // In viewport
                section.classList.add("your-active-class");
            } else {
                // Not in viewport
                section.classList.remove("your-active-class");
            }
        }
    });
}

// Scroll to anchor ID using scrollTO event
function setScrollTo (event) {
    // Register click event in navbar
    navbar.addEventListener("click", function (event) {
        // Get the target id
        const target = document.getElementById(event.target.dataset.nav);
        // Triger the scrollTo event
        target.scrollIntoView();
    });

}

/**
 * End Main Functions
 * Begin Events
 * 
*/

// Build menu 
buildNavebar();
// Scroll to section on link click
setScrollTo();
// Set sections as active
setActive();

