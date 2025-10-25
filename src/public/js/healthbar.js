let fills = document.querySelectorAll(".healthbar_fill");
let hpText = document.querySelector(".hp-text");

let health = 100;
let maxHp = 100;

function renderHealth() {
   let percent = health / maxHp * 100;

   // Update color based on health percentage
   document.documentElement.style.setProperty('--bar-fill', '#00babd');
   document.documentElement.style.setProperty('--bar-top',  '#3cf3f7ff');

   if (percent <= 50) { // yellows
      document.documentElement.style.setProperty('--bar-fill', '#d6ed20');
      document.documentElement.style.setProperty('--bar-top',  '#d8ff48');
   }
   if (percent <= 25) { // reds
      document.documentElement.style.setProperty('--bar-fill', '#ec290a');
      document.documentElement.style.setProperty('--bar-top',  '#ff3818');
   }

   // Update HP text
   hpText.textContent = `HP: ${Math.round(percent)}%`;
   hpText.style.color = getComputedStyle(document.documentElement).getPropertyValue('--bar-fill');

   // Update health bar
   fills.forEach(fill => {
      fill.style.width = percent + "%";
   });
}

function updateHealth(change) {
   health += change;
   health = Math.min(Math.max(health, 0), maxHp);
   renderHealth();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateHealth(0);
});
