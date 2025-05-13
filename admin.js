// Initialize when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();
    
    // Load initial data
    loadGameState();
    
    // Set up event listeners
    document.getElementById('refreshPlayers').addEventListener('click', function() {
        loadGameState();
    });
    
    document.getElementById('refreshBattles').addEventListener('click', function() {
        loadGameState();
    });
    
    document.getElementById('createDeityBtn').addEventListener('click', createDeity);
});

// Function to load game state
async function loadGameState() {
    try {
        const response = await fetch('/api/game_state');
        
        if (!response.ok) {
            throw new Error('Failed to load game state');
        }
        
        const gameState = await response.json();
        
        // Update UI with game state data
        updatePlayersTable(gameState.players);
        updateBattlesTable(gameState.active_battles, gameState.players);
        updateDeitiesTable(gameState.deities, gameState.players);
        updatePlayerSelect(gameState.players);
    } catch (error) {
        console.error('Error loading game state:', error);
        alert('Failed to load game state. Please try again.');
    }
}

// Function to update the players table
function updatePlayersTable(players) {
    const tableBody = document.getElementById('playerTableBody');
    tableBody.innerHTML = '';
    
    if (!players || Object.keys(players).length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="7" class="text-center">No players registered</td>';
        tableBody.appendChild(row);
        return;
    }
    
    for (const [phoneNumber, player] of Object.entries(players)) {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${player.username}</td>
            <td>${player.race}</td>
            <td>${player.class}</td>
            <td>${player.element}</td>
            <td>${player.level}</td>
            <td>${player.rank}</td>
            <td>
                <button class="btn btn-sm btn-info view-player" data-phone="${phoneNumber}">View</button>
                <button class="btn btn-sm btn-warning edit-player" data-phone="${phoneNumber}">Edit</button>
                <button class="btn btn-sm btn-danger delete-player" data-phone="${phoneNumber}">Delete</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    }
    
    // Add event listeners for the view buttons
    document.querySelectorAll('.view-player').forEach(button => {
        button.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('data-phone');
            viewPlayer(phoneNumber);
        });
    });
    
    // Add event listeners for the edit buttons
    document.querySelectorAll('.edit-player').forEach(button => {
        button.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('data-phone');
            editPlayer(phoneNumber);
        });
    });
    
    // Add event listeners for the delete buttons
    document.querySelectorAll('.delete-player').forEach(button => {
        button.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('data-phone');
            if (confirm("Are you sure you want to delete this player? This action cannot be undone.")) {
                deletePlayer(phoneNumber);
            }
        });
    });
}

// Function to update the battles table
function updateBattlesTable(battles, players) {
    const tableBody = document.getElementById('battleTableBody');
    tableBody.innerHTML = '';
    
    if (!battles || Object.keys(battles).length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="5" class="text-center">No active battles</td>';
        tableBody.appendChild(row);
        return;
    }
    
    for (const [battleId, battle] of Object.entries(battles)) {
        const row = document.createElement('tr');
        
        // Get player names for display
        const player1 = players[battle.players[0]] ? players[battle.players[0]].username : 'Unknown';
        const player2 = players[battle.players[1]] ? players[battle.players[1]].username : 'Unknown';
        
        // Get current turn player name
        const currentTurn = players[battle.current_turn] ? players[battle.current_turn].username : 'Unknown';
        
        row.innerHTML = `
            <td>${player1} vs ${player2}</td>
            <td>${battle.zone}</td>
            <td>${currentTurn}</td>
            <td>${battle.rounds}</td>
            <td>
                <button class="btn btn-sm btn-info view-battle" data-id="${battleId}">View</button>
                <button class="btn btn-sm btn-danger end-battle" data-id="${battleId}">End</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    }
    
    // Add event listeners for the view buttons
    document.querySelectorAll('.view-battle').forEach(button => {
        button.addEventListener('click', function() {
            const battleId = this.getAttribute('data-id');
            viewBattle(battleId);
        });
    });
    
    // Add event listeners for the end buttons
    document.querySelectorAll('.end-battle').forEach(button => {
        button.addEventListener('click', function() {
            const battleId = this.getAttribute('data-id');
            if (confirm("Are you sure you want to end this battle?")) {
                endBattle(battleId);
            }
        });
    });
}

// Function to update the deities table
function updateDeitiesTable(deities, players) {
    const tableBody = document.getElementById('deityTableBody');
    tableBody.innerHTML = '';
    
    if (!deities || Object.keys(deities).length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="4" class="text-center">No deities</td>';
        tableBody.appendChild(row);
        return;
    }
    
    for (const [phoneNumber, deity] of Object.entries(deities)) {
        const row = document.createElement('tr');
        
        // Get player name for display
        const playerName = players[deity.player_phone] ? players[deity.player_phone].username : 'Unknown';
        
        row.innerHTML = `
            <td>${deity.name}</td>
            <td>${playerName}</td>
            <td>${deity.chosen ? deity.chosen.length : 0}</td>
            <td>
                <button class="btn btn-sm btn-info view-deity" data-phone="${phoneNumber}">View</button>
                <button class="btn btn-sm btn-warning edit-deity" data-phone="${phoneNumber}">Edit</button>
                <button class="btn btn-sm btn-danger remove-deity" data-phone="${phoneNumber}">Remove</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    }
    
    // Add event listeners for the view buttons
    document.querySelectorAll('.view-deity').forEach(button => {
        button.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('data-phone');
            viewDeity(phoneNumber);
        });
    });
    
    // Add event listeners for the edit buttons
    document.querySelectorAll('.edit-deity').forEach(button => {
        button.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('data-phone');
            editDeity(phoneNumber);
        });
    });
    
    // Add event listeners for the remove buttons
    document.querySelectorAll('.remove-deity').forEach(button => {
        button.addEventListener('click', function() {
            const phoneNumber = this.getAttribute('data-phone');
            if (confirm("Are you sure you want to remove this deity? This action cannot be undone.")) {
                removeDeity(phoneNumber);
            }
        });
    });
}

// Function to update the player select dropdown
function updatePlayerSelect(players) {
    const playerSelect = document.getElementById('playerSelect');
    playerSelect.innerHTML = '<option value="">-- Select Player --</option>';
    
    if (!players || Object.keys(players).length === 0) {
        return;
    }
    
    for (const [phoneNumber, player] of Object.entries(players)) {
        // Skip players who are already deities
        if (player.is_deity) {
            continue;
        }
        
        const option = document.createElement('option');
        option.value = phoneNumber;
        option.textContent = `${player.username} (Level ${player.level} ${player.race} ${player.class})`;
        playerSelect.appendChild(option);
    }
}

// Function to view a player's details
async function viewPlayer(phoneNumber) {
    try {
        const response = await fetch(`/api/player/${phoneNumber}`);
        
        if (!response.ok) {
            throw new Error('Failed to load player data');
        }
        
        const player = await response.json();
        
        // Update the modal with player data
        document.getElementById('playerUsername').textContent = player.username;
        document.getElementById('playerRace').textContent = player.race;
        document.getElementById('playerClass').textContent = player.class;
        document.getElementById('playerElement').textContent = player.element;
        document.getElementById('playerLevel').textContent = player.level;
        document.getElementById('playerRank').textContent = player.rank;
        
        document.getElementById('playerXP').textContent = player.experience;
        document.getElementById('playerGold').textContent = player.gold;
        document.getElementById('playerKarma').textContent = player.karma;
        
        const attributes = player.attributes || {};
        document.getElementById('playerStrength').textContent = attributes.strength || 0;
        document.getElementById('playerAgility').textContent = attributes.agility || 0;
        document.getElementById('playerIntelligence').textContent = attributes.intelligence || 0;
        document.getElementById('playerEndurance').textContent = attributes.endurance || 0;
        
        // Update inventory list
        const inventoryList = document.getElementById('playerInventory');
        inventoryList.innerHTML = '';
        
        if (player.inventory && player.inventory.length > 0) {
            player.inventory.forEach(item => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = item;
                inventoryList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = 'No items';
            inventoryList.appendChild(li);
        }
        
        // Update skills list
        const skillsList = document.getElementById('playerSkills');
        skillsList.innerHTML = '';
        
        if (player.skills && player.skills.length > 0) {
            player.skills.forEach(skill => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = skill;
                skillsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = 'No skills';
            skillsList.appendChild(li);
        }
        
        // Set up edit button
        document.getElementById('editPlayerBtn').setAttribute('data-phone', phoneNumber);
        
        // Show the modal
        const modal = new bootstrap.Modal(document.getElementById('viewPlayerModal'));
        modal.show();
    } catch (error) {
        console.error('Error loading player data:', error);
        alert('Failed to load player data. Please try again.');
    }
}

// Function to edit a player
function editPlayer(phoneNumber) {
    // This would be implemented in a full version
    alert('Edit functionality would be implemented in a full version');
}

// Function to delete a player
function deletePlayer(phoneNumber) {
    // This would be implemented in a full version
    alert('Delete functionality would be implemented in a full version');
}

// Function to view battle details
function viewBattle(battleId) {
    // This would be implemented in a full version
    alert('Battle view functionality would be implemented in a full version');
}

// Function to end a battle
function endBattle(battleId) {
    // This would be implemented in a full version
    alert('End battle functionality would be implemented in a full version');
}

// Function to view deity details
function viewDeity(phoneNumber) {
    // This would be implemented in a full version
    alert('Deity view functionality would be implemented in a full version');
}

// Function to edit a deity
function editDeity(phoneNumber) {
    // This would be implemented in a full version
    alert('Edit deity functionality would be implemented in a full version');
}

// Function to remove a deity
function removeDeity(phoneNumber) {
    // This would be implemented in a full version
    alert('Remove deity functionality would be implemented in a full version');
}

// Function to create a new deity
async function createDeity() {
    const deityName = document.getElementById('deityName').value.trim();
    const playerPhone = document.getElementById('playerSelect').value;
    
    if (!deityName) {
        alert('Please enter a deity name');
        return;
    }
    
    if (!playerPhone) {
        alert('Please select a player');
        return;
    }
    
    try {
        const response = await fetch('/api/create_deity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: deityName,
                phone: playerPhone
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create deity');
        }
        
        // Close the modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createDeityModal'));
        modal.hide();
        
        // Reload game state
        loadGameState();
        
        // Show success message
        alert('Deity created successfully');
    } catch (error) {
        console.error('Error creating deity:', error);
        alert('Failed to create deity. Please try again.');
    }
}
