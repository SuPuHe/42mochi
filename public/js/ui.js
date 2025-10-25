function toggleModal(modalId) {
    const storeModal = document.getElementById('store-modal');
    const inventoryModal = document.getElementById('inventory-modal');

    if (modalId === 'store') {
        if (!inventoryModal.classList.contains('hidden')) {
            inventoryModal.classList.add('hidden');
        }
        storeModal.classList.toggle('hidden');

        if (!storeModal.classList.contains('hidden')) {
            openTab('store-food');
        }

    } else if (modalId === 'inventory') {
        if (!storeModal.classList.contains('hidden')) {
            storeModal.classList.add('hidden');
        }
        inventoryModal.classList.toggle('hidden');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(`${modalId}-modal`);
    if (modal) {
        modal.classList.add('hidden');
    }
}

function closeAllModals() {
    const storeModal = document.getElementById('store-modal');
    const inventoryModal = document.getElementById('inventory-modal');
    if (storeModal) storeModal.classList.add('hidden');
    if (inventoryModal) inventoryModal.classList.add('hidden');
}

function openTab(tabId) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));

    const tabButtons = document.querySelectorAll('.store-tabs .tab-button');
    tabButtons.forEach(button => button.classList.remove('active'));

    const activeContent = document.getElementById(tabId);
    if (activeContent) {
        activeContent.classList.add('active');
    }

    const activeTabButton = document.querySelector(`.store-tabs button[onclick*="${tabId}"]`);
    if (activeTabButton) {
        activeTabButton.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    openTab('store-food');

    // Close modals when clicking outside of modal content
    const storeModal = document.getElementById('store-modal');
    const inventoryModal = document.getElementById('inventory-modal');

    if (storeModal) {
        storeModal.addEventListener('click', (e) => {
            // If clicking on the modal backdrop (not the content), close it
            if (e.target === storeModal) {
                closeModal('store');
            }
        });
    }

    if (inventoryModal) {
        inventoryModal.addEventListener('click', (e) => {
            // If clicking on the modal backdrop (not the content), close it
            if (e.target === inventoryModal) {
                closeModal('inventory');
            }
        });
    }

    // Close modals with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
});
