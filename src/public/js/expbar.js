// Select all experience bar fill elements and the text display
let expFills = document.querySelectorAll(".expbar_fill");
let expText = document.querySelector(".lvl-text");

// Initialize experience values
let experience = 50;
let maxExp = 100;

/**
 * Renders the current experience state to the UI
 * Updates the fill color, width of the bar, and text display
 */
function renderExp() {
   let percent = experience / maxExp * 100;

   // Set the blue color scheme for the experience bar
   // Can be extended to show different shades based on exp milestones
   document.documentElement.style.setProperty('--exp-fill', '#00babd');
   document.documentElement.style.setProperty('--exp-top',  '#2ee7ebff');

   // Update the experience text and match its color to the bar
   expText.textContent = `EXP: ${Math.round(percent)}%`;
   expText.style.color = getComputedStyle(document.documentElement).getPropertyValue('--exp-fill');

   // Update the width of all fill elements to show current progress
   expFills.forEach(fill => {
      fill.style.width = percent + "%";
   });
}

/**
 * Updates the experience value and triggers a render
 * @param {number} change - Amount to change experience by (positive or negative)
 */
function updateExp(change) {
   experience += change;
   if (experience >= maxExp) {
       // Can be extended to trigger level up events
       experience = experience % maxExp;
   }
   // Ensure experience doesn't go below 0
   experience = Math.max(experience, 0);
   renderExp();
}

// Initialize the experience bar when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    updateExp(0);
});
