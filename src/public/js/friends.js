document.addEventListener("DOMContentLoaded", () => {
  const friendsList = document.querySelector(".friends-list");
  const requestsList = document.querySelector(".requests-list");

  // --- MODAL HANDLERS ---
  window.openAddFriendModal = function () {
    document.getElementById("addFriendModalOverlay").style.display = "flex";
  };

  window.closeModal = function (event) {
    if (!event || event.target.classList.contains("modal-overlay") || event.target.tagName === "BUTTON") {
      document.getElementById("addFriendModalOverlay").style.display = "none";
    }
  };

  window.addFriend = function (event) {
    event.preventDefault();
    const name = document.getElementById("friendIntra").value.trim();
    if (!name) return alert("Enter an intraname.");

    // Create "pending" request dynamically
    const card = document.createElement("div");
    card.className = "request-card";
    card.innerHTML = `You sent a request to <strong>${name}</strong> — pending.`;
    requestsList.appendChild(card);

    alert(`Friend request sent to ${name}!`);
    document.getElementById("friendIntra").value = "";
    closeModal();
  };

  // --- ACCEPT / DECLINE HANDLERS ---
  requestsList.addEventListener("click", (e) => {
    if (e.target.classList.contains("accept")) {
      const card = e.target.closest(".request-card");
      const name = card.querySelector("strong").textContent;

      // Create a new friend entry
      const newFriend = document.createElement("div");
      newFriend.className = "friend-card online";
      newFriend.innerHTML = `
        <span class="avatar">🧑‍💻</span>
        <div class="friend-info">
          <strong>${name}</strong>
          <small>Lvl ${Math.floor(Math.random() * 10) + 1} • Online</small>
        </div>
        <span class="status-dot green"></span>
      `;

      friendsList.appendChild(newFriend);
      card.remove(); // Remove request
    }

    if (e.target.classList.contains("decline")) {
      const card = e.target.closest(".request-card");
      card.remove();
    }
  });
});
