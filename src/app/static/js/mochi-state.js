// Mochi State Management
const mochiState = {
    hp: 100,
    exp: 50,
    coins: 100,
    inventory: {}
};

async function fetchMochiStats() {
    try {
        const response = await fetch('/api/getMochiStats');
        const data = await response.json();
        mochiState.hp = data.hp;
        mochiState.exp = data.days; // Assuming 'days' is used as EXP
        mochiState.coins = data.coins;
        mochiState.inventory.int_food = data.int_food;
        mochiState.inventory.char_food = data.char_food;
        updateUI();
        addConsoleLog('State refreshed from server', 'info');
    } catch (error) {
        addConsoleLog(`✗ Failed to fetch stats: ${error.message}`, 'error');
        console.error('Failed to fetch Mochi stats:', error);
    }
}

function updateUI() {
    // Update HP bar
    const health = mochiState.hp;
    const maxHp = 100;
    const percent = health / maxHp * 100;
    document.querySelector('.hp-text').textContent = `HP: ${Math.round(percent)}%`;
    document.querySelectorAll('.healthbar_fill').forEach(fill => {
        fill.style.width = percent + "%";
    });
    
    // Update character animation based on HP
    if (window.character) {
        window.character.updateHP(health);
    }
    
    // Get coalition colors from CSS variables
    const rootStyles = getComputedStyle(document.documentElement);
    const coalitionColor = rootStyles.getPropertyValue('--coalition-color').trim() || '#00babd';
    const coalitionColorLight = rootStyles.getPropertyValue('--coalition-color-light').trim() || '#69ecee';
    
    // Change colors based on health percentage (check from lowest to highest)
    if (percent <= 25) {
        // Red critical color when health is very low
        document.documentElement.style.setProperty('--bar-fill', '#ec290a');
        document.documentElement.style.setProperty('--bar-top',  '#ff3818');
    } else if (percent <= 50) {
        // Yellow warning color when health is low
        document.documentElement.style.setProperty('--bar-fill', '#d6ed20');
        document.documentElement.style.setProperty('--bar-top',  '#d8ff48');
    } else {
        // Use coalition colors when health is good (> 50%)
        document.documentElement.style.setProperty('--bar-fill', coalitionColor);
        document.documentElement.style.setProperty('--bar-top',  coalitionColorLight);
    }


    // Update Days Alive
    const daysText = document.querySelector('.days-text');
    if (daysText) {
        daysText.textContent = `Days Alive: ${mochiState.exp}`;
    }

    // Update Coins
    document.querySelector('.coin-amount').textContent = mochiState.coins;

    // Update Inventory
    updateInventoryUI();
    
    // Update Console Output
    updateConsoleOutput();
}

function updateConsoleOutput() {
    const consoleContent = document.getElementById('console-content');
    if (!consoleContent) return;
    
    const timestamp = new Date().toLocaleTimeString();
    
    consoleContent.innerHTML = `
        <div class="console-line">> [${timestamp}] Mochi State Updated</div>
        <div class="console-line">==========================================</div>
        <div class="console-line success">> HP: ${mochiState.hp}/100 (${Math.round(mochiState.hp)}%)</div>
        <div class="console-line info">> Days Alive: ${mochiState.exp}</div>
        <div class="console-line warning">> Coins: ${mochiState.coins} 💰</div>
        <div class="console-line">==========================================</div>
        <div class="console-line">> Inventory Status:</div>
        <div class="console-line">  - Int Soup 🥣: ${mochiState.inventory.int_food || 0}</div>
        <div class="console-line">  - Char Cookies 🍪: ${mochiState.inventory.char_food || 0}</div>
        <div class="console-line">==========================================</div>
        <div class="console-line">> Health Status: ${getHealthStatus(mochiState.hp)}</div>
        <div class="console-line">> Coin Status: ${getCoinStatus(mochiState.coins)}</div>
    `;
}

function getHealthStatus(hp) {
    if (hp >= 80) return '✓ Excellent';
    if (hp >= 50) return '~ Good';
    if (hp >= 25) return '⚠ Warning';
    return '✗ Critical!';
}

function getCoinStatus(coins) {
    if (coins >= 100) return '✓ Rich';
    if (coins >= 50) return '~ Moderate';
    if (coins >= 10) return '⚠ Low';
    return '✗ Poor!';
}

function addConsoleLog(message, type = '') {
    const consoleContent = document.getElementById('console-content');
    if (!consoleContent) return;
    
    const timestamp = new Date().toLocaleTimeString();
    const logLine = document.createElement('div');
    logLine.className = `console-line ${type}`;
    logLine.textContent = `> [${timestamp}] ${message}`;
    
    // Add at the top
    consoleContent.insertBefore(logLine, consoleContent.firstChild);
    
    // Keep only last 20 lines
    while (consoleContent.children.length > 20) {
        consoleContent.removeChild(consoleContent.lastChild);
    }
}

function updateInventoryUI() {
    const inventoryGrid = document.querySelector('.inventory-grid');
    inventoryGrid.innerHTML = ''; // Clear current inventory

    for (const itemKey in mochiState.inventory) {
        const count = mochiState.inventory[itemKey];
        if (count > 0) {
            const itemDetails = getItemDetails(itemKey);
            const inventoryItem = document.createElement('div');
            inventoryItem.classList.add('inventory-item');
            inventoryItem.innerHTML = `
                <span class="item-icon">${itemDetails.icon}</span>
                <span class="item-name">${itemDetails.name}</span>
                <span class="item-count">x${count}</span>
                <button class="eat-button" data-item="${itemKey}">Eat</button>
            `;
            inventoryGrid.appendChild(inventoryItem);
        }
    }
}

function getItemDetails(itemKey) {
    switch (itemKey) {
        case 'int_food':
            return { name: 'Int Soup', icon: '🥣' };
        case 'char_food':
            return { name: 'Char Cookies', icon: '🍪' };
        default:
            return { name: 'Unknown', icon: '❓' };
    }
}

async function buyItem(item, price) {
    const itemDetails = getItemDetails(item);
    addConsoleLog(`Attempting to buy ${itemDetails.name} ${itemDetails.icon} for ${price} coins...`, 'info');
    console.log('Attempting to buy:', item, 'for', price, 'coins');
    console.log('Current coins:', mochiState.coins);

    try {
        const response = await fetch('/api/buyFood', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ food_type: item, price: price })
        });

        const responseData = await response.json();
        console.log('Server response:', responseData);

        if (response.ok) {
            addConsoleLog(`✓ Purchased ${itemDetails.name} ${itemDetails.icon} (-${price} coins)`, 'success');
            console.log('Purchase successful! Refreshing stats...');
            await fetchMochiStats(); // Refresh data after purchase
        } else {
            addConsoleLog(`✗ Purchase failed: ${responseData.error || 'Not enough coins!'}`, 'error');
            alert(responseData.error || 'Not enough coins!');
        }
    } catch (error) {
        addConsoleLog(`✗ Error buying item: ${error.message}`, 'error');
        console.error('Failed to buy item:', error);
    }
}

async function eatItem(item) {
    const itemDetails = getItemDetails(item);
    const hp_amount = (item === 'int_food') ? 15 : 10;
    addConsoleLog(`Feeding Mochi with ${itemDetails.name} ${itemDetails.icon}...`, 'info');
    
    try {
        const response = await fetch('/api/eatFood', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ food_type: item, hp_amount: hp_amount })
        });
        if (response.ok) {
            addConsoleLog(`✓ Mochi ate ${itemDetails.name} ${itemDetails.icon} (+${hp_amount} HP)`, 'success');
            fetchMochiStats(); // Refresh data after eating
        } else {
            const errorData = await response.json();
            addConsoleLog(`✗ Feeding failed: ${errorData.error || 'Failed to eat item'}`, 'error');
            alert(errorData.error || 'Failed to eat item.');
        }
    } catch (error) {
        addConsoleLog(`✗ Error feeding: ${error.message}`, 'error');
        console.error('Failed to eat item:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('mochi-state.js loaded');
    
    // Initialize HP bar colors with coalition colors
    const rootStyles = getComputedStyle(document.documentElement);
    const coalitionColor = rootStyles.getPropertyValue('--coalition-color').trim() || '#00babd';
    const coalitionColorLight = rootStyles.getPropertyValue('--coalition-color-light').trim() || '#69ecee';
    document.documentElement.style.setProperty('--bar-fill', coalitionColor);
    document.documentElement.style.setProperty('--bar-top', coalitionColorLight);
    
    // Initialize console
    addConsoleLog('=== 42Mochi System Initialized ===', 'success');
    
    // Log sprite type
    const canvas = document.getElementById('characterCanvas');
    const spriteType = canvas?.dataset.spriteType || 'green';
    addConsoleLog(`Loading ${spriteType} Mochi sprite...`, 'info');
    
    addConsoleLog('Loading Mochi state from server...', 'info');

    // Initial fetch
    fetchMochiStats();

    // Set up periodic fetching
    setInterval(fetchMochiStats, 5000);

    // Event delegation for buy buttons (they're inside a modal that might not be visible at load)
    document.body.addEventListener('click', (e) => {
        console.log('Click detected on:', e.target, 'Classes:', e.target.classList);

        // Check if the clicked element is a buy button
        if (e.target.classList.contains('buy-button')) {
            console.log('✅ Buy button clicked!');
            e.preventDefault();
            e.stopPropagation();

            const storeItem = e.target.closest('.store-item');
            console.log('Store item found:', storeItem);

            if (!storeItem) {
                console.error('❌ Could not find parent .store-item');
                return;
            }

            const item = storeItem.dataset.item;
            const price = parseInt(storeItem.dataset.price);

            console.log('📦 Item:', item, 'Price:', price);
            console.log('💰 Current coins before purchase:', mochiState.coins);
            buyItem(item, price);
        }
    }, true); // Use capture phase to catch events before they bubble

    // Event listener for eat buttons (using event delegation)
    document.body.addEventListener('click', (e) => {
        if (e.target.classList.contains('eat-button')) {
            e.preventDefault();
            e.stopPropagation();
            const item = e.target.dataset.item;
            console.log('Eating item:', item);
            eatItem(item);
        }
    });
});

