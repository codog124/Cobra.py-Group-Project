/**
 * Toggles the display of an individual team member's bio
 * @param {string} bioId - The ID of the bio section to show or hide
 */
function toggleBio(bioId, imgId) {
    const bio = document.getElementById(bioId);
    const img = document.getElementById(imgId);

    const isHidden = window.getComputedStyle(bio).display === "none";

    if (isHidden) {
        bio.style.display = "block";
        if (img) img.style.display = "block";
    } else {
        bio.style.display = "none";
        if (img) img.style.display = "none";
    }
}

/**
 * Shows the specified section ('bios' or 'vision') and hides the other
 * @param {string} sectionId - The ID of the section to display
 */
function showSection(sectionId) {
    const biosSection = document.getElementById("bios");
    const visionSection = document.getElementById("vision");

    // Display the bios section and hide the vision section
    if (sectionId === "bios") {
        biosSection.style.display = "flex";
        visionSection.style.display = "none";
    }
    // Display the vision section and hide the bios section
    else if (sectionId === "vision") {
        biosSection.style.display = "none";
        visionSection.style.display = "block";
    }
}
