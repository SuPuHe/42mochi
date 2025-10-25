document.addEventListener("DOMContentLoaded", () => {
  const viewModalOverlay = document.getElementById("viewModalOverlay");
  const createModalOverlay = document.getElementById("createModalOverlay");

  // --- Modal Handlers ---
  window.openViewModal = function (project, author, content) {
    document.getElementById("modalProject").textContent = project;
    document.getElementById("modalAuthor").textContent = author;
    document.getElementById("modalContent").textContent = content;
    viewModalOverlay.style.display = "flex";
  };

  window.openCreateModal = function () {
    createModalOverlay.style.display = "flex";
  };

  window.closeModal = function (event) {
    // Close when clicking outside or any button
    if (!event || event.target.classList.contains("modal-overlay") || event.target.tagName === "BUTTON") {
      viewModalOverlay.style.display = "none";
      createModalOverlay.style.display = "none";
    }
  };

  // --- Form Submission ---
  window.submitPost = function (event) {
    event.preventDefault();

    const project = document.getElementById("projectName").value.trim();
    const summary = document.getElementById("projectSummary").value.trim();
    const details = document.getElementById("projectDetails").value.trim();

    if (!project || !summary || !details) {
      alert("Please fill out all fields before submitting.");
      return;
    }

    console.log("🆕 New Post Created:", { project, summary, details });
    alert(`New post for ${project} created!`);

    // Reset and close modal
    event.target.reset();
    closeModal();
  };
});
