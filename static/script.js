/**
 * JavaScript functions.
 *
 * script.js
 */


/* Get current year for copyright. */

function getCurrentYear() {
    const currentDate = new Date();
    return currentDate.getFullYear();
}


/* Redirect to other pages. */

function redirectTo(route) {
    window.location.href = route;
}