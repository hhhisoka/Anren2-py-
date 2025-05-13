import random
import logging
from typing import Dict, List, Tuple, Any

# Initialize logger
logger = logging.getLogger(__name__)

# Game constants
RACES = ["Human", "Elf", "Dwarf", "Orc", "Anaon"]
CLASSES = ["Warrior", "Archer", "Mage", "Paladin", "Rogue", "Druid", "Necromancer", 
           "Bard", "Berserker", "Alchemist", "Guardian", "Scout", "Chronomancer", "Artisan"]
ELEMENTS = ["Fire", "Water", "Plant", "Earth", "Wind", "Darkness", "Light"]
ZONES = ["Forest", "Volcano", "Ocean", "Mountain", "Sky"]
RANKS = ["G", "F", "E", "D", "C", "B", "A", "S", "SS"]
SKILLS = ["Punch", "Mind Shuffle", "Precision Shot", "Minor Heal", "Magic Shield"]

# Race trait bonuses
RACE_TRAITS = {
    "Human": {"exp_gain": 0.05},
    "Elf": {"dodge": 0.10, "endurance": -0.05},
    "Dwarf": {"defense": 0.15, "speed": -0.10},
    "Orc": {"melee_damage": 0.20, "intelligence": -0.10},
    "Anaon": {"dark_magic": 0.15, "max_hp": -0.10}
}

# Class bonuses
CLASS_BONUSES = {
    "Warrior": {"melee_damage": 0.15, "endurance": 10},
    "Archer": {"range_damage": 0.15, "agility": 10},
    "Mage": {"magic_power": 0.20, "intelligence": 10},
    "Paladin": {"defense": 0.10, "healing": 0.05, "endurance": 10},
    "Rogue": {"dodge": 0.20, "crit": 0.20, "agility": 10},
    "Druid": {"healing": 0.15, "nature_control": 0.15, "intelligence": 5, "strength": 5},
    "Necromancer": {"summon": 0.15, "life_leech": 0.10, "dark_magic": 10},
    "Bard": {"support": 0.20, "party_buffs": 0.15, "charisma": 10, "agility": 5},
    "Berserker": {"rage": 0.25, "defense": -0.15, "strength": 10, "endurance": 10},
    "Alchemist": {"potions": 0.20, "bombs": 0.15, "intelligence": 10, "constitution": 5},
    "Guardian": {"ally_protection": 0.20, "magic_barriers": 0.15, "defense": 10, "endurance": 10},
    "Scout": {"reconnaissance": 0.20, "traps": 0.15, "agility": 10, "intelligence": 5},
    "Chronomancer": {"time_manipulation": 0.20, "magic": 0.15, "intelligence": 10},
    "Artisan": {"crafting": 0.25, "upgrade": 0.20, "commerce": 10, "constitution": 5}
}

# Racial synergies
RACIAL_SYNERGIES = {
    "Human": {"exp_gain": 0.05},
    "Elf": {"ranged_damage": 0.10, "magic_damage": 0.10},
    "Dwarf": {"Warrior": {"defense": 0.10}, "Paladin": {"defense": 0.10}},
    "Orc": {"Warrior": {"melee_damage": 0.10, "crit_damage": 0.10}, 
            "Berserker": {"melee_damage": 0.10, "crit_damage": 0.10}},
    "Anaon": {"Rogue": {"dark_magic": 0.10, "stealth": 0.10}, 
              "Necromancer": {"dark_magic": 0.10, "stealth": 0.10}}
}

# Element advantages
ELEMENT_ADVANTAGES = {
    "Fire": {"advantage": "Plant", "disadvantage": "Water"},
    "Water": {"advantage": "Fire", "disadvantage": "Plant"},
    "Plant": {"advantage": "Water", "disadvantage": "Fire"},
    "Earth": {"advantage": "Wind", "disadvantage": "Water"},
    "Wind": {"advantage": "Earth", "disadvantage": "Fire"},
    "Light": {"advantage": "Darkness", "disadvantage": ""},
    "Darkness": {"advantage": "Light", "disadvantage": ""}
}

# Zone effects
ZONE_EFFECTS = {
    "Forest": {"Plant": {"damage": 0.10}, "Fire": {"defense": -0.10}},
    "Volcano": {"Fire": {"attack_speed": 0.15}, "Water": {"resistance": -0.15}},
    "Ocean": {"Water": {"max_hp": 0.10}, "Plant": {"dodge": -0.10}},
    "Mountain": {"Earth": {"endurance": 0.10}, "Wind": {"agility": -0.10}},
    "Sky": {"Wind": {"dodge": 0.12}, "Earth": {"accuracy": -0.12}}
}

# Rank stats and rewards
RANK_BONUSES = {
    "G": {"max_stats": 100, "exp_gain": 0.05},
    "F": {"max_stats": 150, "gold_gain": 0.05},
    "E": {"max_stats": 200, "karma_gain": 0.05},
    "D": {"max_stats": 250, "exp_gain": 0.10},
    "C": {"max_stats": 300, "gold_gain": 0.10},
    "B": {"max_stats": 350, "karma_gain": 0.10},
    "A": {"max_stats": 400, "exp_gain": 0.15, "summons": True},
    "S": {"max_stats": 450, "gold_gain": 0.15, "ascensions": True},
    "SS": {"max_stats": 500, "karma_gain": 0.20, "divine_raids": True}
}

# Starting items by class
CLASS_ITEMS = {
    "Warrior": ["Iron Axe", "Steel Shield"],
    "Archer": ["Wooden Bow", "Quiver of 20 Arrows"],
    "Mage": ["Carved Wooden Staff", "Basic Spellbook"],
    "Paladin": ["Blessed Shortsword", "Major Healing Potion"],
    "Rogue": ["Light Dagger", "Shadow Cloak"],
    "Druid": ["Sacred Branch", "5x Healing Herbs"],
    "Necromancer": ["Rat Skull", "Tome of Necromancy"],
    "Bard": ["Lute", "Enchanted Flute"],
    "Berserker": ["Rusty Hatchet", "Rage Flask"],
    "Alchemist": ["Basic Alchemy Kit", "3x Smoke Bombs"],
    "Guardian": ["Guard's Hammer", "Magic Barrier Scroll"],
    "Scout": ["Spyglass", "2x Mechanical Traps"],
    "Chronomancer": ["Mystic Hourglass", "Enchanted Pocket Watch"],
    "Artisan": ["Portable Anvil", "Blacksmith's Hammer"]
}

def process_game_command(command: str, player_phone: str, game_state: Dict) -> str:
    """Process a game command and return the response"""
    command = command.lower().strip()
    parts = command.split()
    
    # Check if player exists
    if player_phone in game_state["players"]:
        player = game_state["players"][player_phone]
    else:
        # If player doesn't exist, only allow registration or help
        if command.startswith("register"):
            return register_player(parts, player_phone, game_state)
        elif command == "help":
            return get_help_text()
        else:
            return "You are not registered. Use 'register [username] [race] [class] [element]' to join the game."
    
    # Process command for registered player
    if command.startswith("help"):
        return get_help_text()
    elif command.startswith("status"):
        return get_player_status(player)
    elif command.startswith("inventory"):
        return get_player_inventory(player)
    elif command.startswith("skills"):
        return get_player_skills(player)
    elif command.startswith("duel"):
        return initiate_duel(parts, player, player_phone, game_state)
    elif command.startswith("attack"):
        return process_attack(parts, player, player_phone, game_state)
    elif command.startswith("use"):
        return use_item_or_skill(parts, player, player_phone, game_state)
    elif command.startswith("shop"):
        return show_shop_items(player)
    elif command.startswith("buy"):
        return buy_item(parts, player, game_state)
    elif command.startswith("explore"):
        return explore_zone(parts, player, game_state)
    elif command.startswith("quest"):
        return manage_quests(parts, player, game_state)
    elif command.startswith("rank"):
        return show_rank_info(player)
    else:
        return "Unknown command. Type 'help' for available commands."

def register_player(parts: List[str], phone: str, game_state: Dict) -> str:
    """Register a new player"""
    if len(parts) < 5:
        return "Registration format: register [username] [race] [class] [element]"
    
    username = parts[1]
    race = parts[2].capitalize()
    char_class = parts[3].capitalize()
    element = parts[4].capitalize()
    
    # Validate inputs
    if race not in RACES:
        return f"Invalid race. Choose from: {', '.join(RACES)}"
    
    if char_class not in CLASSES:
        return f"Invalid class. Choose from: {', '.join(CLASSES)}"
    
    if element not in ELEMENTS:
        return f"Invalid element. Choose from: {', '.join(ELEMENTS)}"
    
    # Check if username is taken
    for p_phone, p_data in game_state["players"].items():
        if p_data["username"].lower() == username.lower():
            return "Username already taken. Please choose another."
    
    # Create new player
    new_player = {
        "username": username,
        "race": race,
        "class": char_class,
        "element": element,
        "level": 1,
        "experience": 0,
        "gold": 100,
        "karma": 0,
        "rank": "G",
        "attributes": {
            "strength": 0,
            "agility": 0,
            "intelligence": 0,
            "endurance": 0
        },
        "skills": ["Punch"],  # Default starter skill
        "inventory": [],
        "equipped": {},
        "is_deity": False,
        "in_battle": False
    }
    
    # Add a starting item based on class
    if char_class in CLASS_ITEMS:
        new_player["inventory"].append(CLASS_ITEMS[char_class][0])
    
    # Ask for attribute distribution
    attribute_setup_message = (
        f"Welcome {username}, the {race} {char_class}!\n"
        "You have 10 points to distribute among your attributes.\n"
        "Use 'attributes [str] [agi] [int] [end]' to set them.\n"
        "Example: attributes 4 2 2 2"
    )
    
    # Add player to game state
    game_state["players"][phone] = new_player
    
    return attribute_setup_message

def get_help_text() -> str:
    """Return the help text with available commands"""
    return (
        "🎮 WHATSAPP RPG - COMMAND GUIDE 🎮\n\n"
        "GENERAL COMMANDS:\n"
        "- help: Show this help\n"
        "- status: Check your character status\n"
        "- inventory: View your items\n"
        "- skills: List your skills\n\n"
        
        "REGISTRATION:\n"
        "- register [username] [race] [class] [element]: Create character\n"
        "- attributes [str] [agi] [int] [end]: Set attributes\n\n"
        
        "COMBAT:\n"
        "- duel [player]: Challenge someone to a duel\n"
        "- attack [skill]: Use a skill in combat\n"
        "- use [item/skill]: Use an item or skill\n\n"
        
        "EXPLORATION:\n"
        "- explore [zone]: Explore a zone\n"
        "- quest [id]: Start a quest\n\n"
        
        "ECONOMY:\n"
        "- shop: View available items\n"
        "- buy [item]: Purchase an item\n\n"
        
        "PROGRESSION:\n"
        "- rank: View rank information\n\n"
        
        "Available races: Human, Elf, Dwarf, Orc, Anaon\n"
        "Available classes: Warrior, Archer, Mage, Paladin, Rogue, Druid, Necromancer, "
        "Bard, Berserker, Alchemist, Guardian, Scout, Chronomancer, Artisan\n"
        "Available elements: Fire, Water, Plant, Earth, Wind, Darkness, Light"
    )

def get_player_status(player: Dict) -> str:
    """Return player status information"""
    attributes = player["attributes"]
    
    status = (
        f"📊 STATUS: {player['username']} 📊\n\n"
        f"Level {player['level']} {player['race']} {player['class']}\n"
        f"Element: {player['element']}\n"
        f"Rank: {player['rank']}\n\n"
        f"XP: {player['experience']}\n"
        f"Gold: {player['gold']}\n"
        f"Karma: {player['karma']}\n\n"
        f"ATTRIBUTES:\n"
        f"- Strength: {attributes['strength']}\n"
        f"- Agility: {attributes['agility']}\n"
        f"- Intelligence: {attributes['intelligence']}\n"
        f"- Endurance: {attributes['endurance']}\n\n"
        f"Type 'skills' or 'inventory' for more info."
    )
    
    return status

def get_player_inventory(player: Dict) -> str:
    """Return player inventory"""
    if not player["inventory"]:
        return "Your inventory is empty."
    
    inventory_text = "🎒 INVENTORY 🎒\n\n"
    for item in player["inventory"]:
        inventory_text += f"- {item}\n"
    
    return inventory_text

def get_player_skills(player: Dict) -> str:
    """Return player skills"""
    if not player["skills"]:
        return "You don't have any skills yet."
    
    skills_text = "⚔️ SKILLS ⚔️\n\n"
    for skill in player["skills"]:
        skills_text += f"- {skill}\n"
    
    return skills_text

def initiate_duel(parts: List[str], player: Dict, player_phone: str, game_state: Dict) -> str:
    """Initiate a duel with another player"""
    if len(parts) < 2:
        return "Please specify a player to duel. Example: duel [player]"
    
    target_username = parts[1]
    
    # Find target player
    target_phone = None
    target_player = None
    
    for phone, p in game_state["players"].items():
        if p["username"].lower() == target_username.lower():
            target_phone = phone
            target_player = p
            break
    
    if not target_player:
        return f"Player '{target_username}' not found."
    
    if target_phone == player_phone:
        return "You can't duel yourself."
    
    if player["in_battle"] or target_player["in_battle"]:
        return "Either you or your target is already in a battle."
    
    # Create a new battle
    battle_id = f"{player_phone}_{target_phone}"
    
    game_state["active_battles"][battle_id] = {
        "players": [player_phone, target_phone],
        "current_turn": player_phone,
        "rounds": 0,
        "logs": [f"{player['username']} challenged {target_player['username']} to a duel!"],
        "zone": random.choice(ZONES)
    }
    
    # Mark players as in battle
    player["in_battle"] = True
    target_player["in_battle"] = True
    
    return (
        f"You challenged {target_player['username']} to a duel in the {game_state['active_battles'][battle_id]['zone']}!\n"
        f"Use 'attack [skill]' to make your move."
    )

def process_attack(parts: List[str], player: Dict, player_phone: str, game_state: Dict) -> str:
    """Process an attack in a duel"""
    if not player["in_battle"]:
        return "You're not in a battle."
    
    # Find the active battle
    battle_id = None
    battle = None
    
    for b_id, b_data in game_state["active_battles"].items():
        if player_phone in b_data["players"]:
            battle_id = b_id
            battle = b_data
            break
    
    if not battle:
        # Something went wrong, reset battle state
        player["in_battle"] = False
        return "You're not in an active battle. Your status has been reset."
    
    if battle["current_turn"] != player_phone:
        return "It's not your turn to attack."
    
    # Get skill to use
    skill = "Punch"  # Default skill
    if len(parts) >= 2:
        requested_skill = " ".join(parts[1:])
        for s in player["skills"]:
            if s.lower() == requested_skill.lower():
                skill = s
                break
    
    # Find opponent
    opponent_phone = battle["players"][0] if battle["players"][1] == player_phone else battle["players"][1]
    opponent = game_state["players"][opponent_phone]
    
    # Calculate damage based on attributes, skills, and bonuses
    damage = calculate_damage(player, opponent, skill, battle["zone"])
    
    # Apply damage to opponent (this is simplified, would need HP system)
    battle["logs"].append(f"{player['username']} used {skill} and dealt {damage} damage!")
    
    # Switch turn
    battle["current_turn"] = opponent_phone
    battle["rounds"] += 1
    
    # Check if battle should end (for this example, we'll end after 5 rounds)
    if battle["rounds"] >= 5:
        # Determine winner based on total damage (simplified)
        battle["logs"].append(f"The duel has ended! {player['username']} wins!")
        
        # End battle
        player["in_battle"] = False
        opponent["in_battle"] = False
        
        # Award winner
        player["experience"] += 50
        player["gold"] += 10
        
        # Check for level up
        check_level_up(player)
        
        # Remove battle
        del game_state["active_battles"][battle_id]
        
        battle_log = "\n".join(battle["logs"])
        return f"{battle_log}\n\nYou won the duel and gained 50 XP and 10 gold!"
    
    return f"You used {skill}! Waiting for {opponent['username']} to make their move."

def calculate_damage(attacker: Dict, defender: Dict, skill: str, zone: str) -> int:
    """Calculate damage for an attack (simplified)"""
    # Base damage based on strength or intelligence depending on skill
    if skill in ["Punch", "Precision Shot"]:
        base_damage = 5 + (attacker["attributes"]["strength"] * 2)
    else:
        base_damage = 5 + (attacker["attributes"]["intelligence"] * 2)
    
    # Apply racial bonuses
    if attacker["race"] in RACE_TRAITS:
        traits = RACE_TRAITS[attacker["race"]]
        if "melee_damage" in traits and skill == "Punch":
            base_damage *= (1 + traits["melee_damage"])
    
    # Apply class bonuses
    if attacker["class"] in CLASS_BONUSES:
        bonuses = CLASS_BONUSES[attacker["class"]]
        if "melee_damage" in bonuses and skill == "Punch":
            base_damage *= (1 + bonuses["melee_damage"])
        elif "magic_power" in bonuses and skill in ["Mind Shuffle", "Magic Shield"]:
            base_damage *= (1 + bonuses["magic_power"])
    
    # Apply element advantages
    if attacker["element"] in ELEMENT_ADVANTAGES and defender["element"] == ELEMENT_ADVANTAGES[attacker["element"]]["advantage"]:
        base_damage *= 1.1  # 10% more damage
    
    # Apply zone effects
    if zone in ZONE_EFFECTS and attacker["element"] in ZONE_EFFECTS[zone]:
        element_effects = ZONE_EFFECTS[zone][attacker["element"]]
        if "damage" in element_effects:
            base_damage *= (1 + element_effects["damage"])
    
    # Random variance (±10%)
    variance = random.uniform(0.9, 1.1)
    
    return round(base_damage * variance)

def check_level_up(player: Dict) -> bool:
    """Check if player levels up and apply if needed"""
    exp_required = player["level"] * 100
    
    if player["experience"] >= exp_required:
        player["level"] += 1
        player["experience"] -= exp_required
        
        # Update rank if needed
        rank_index = RANKS.index(player["rank"])
        if player["level"] >= 10 * (rank_index + 1) and rank_index < len(RANKS) - 1:
            player["rank"] = RANKS[rank_index + 1]
        
        return True
    
    return False

def use_item_or_skill(parts: List[str], player: Dict, player_phone: str, game_state: Dict) -> str:
    """Use an item or skill outside of combat"""
    if len(parts) < 2:
        return "Please specify what to use. Example: use [item/skill]"
    
    item_or_skill = " ".join(parts[1:])
    
    # Check if it's an item
    if item_or_skill in player["inventory"]:
        # Apply item effect
        # This is a simplified version, real implementation would have different effects
        if "Potion" in item_or_skill:
            player["inventory"].remove(item_or_skill)
            return f"You used {item_or_skill}. You feel refreshed!"
        else:
            return f"You can't use {item_or_skill} right now."
    
    # Check if it's a skill
    if item_or_skill in player["skills"]:
        # Some skills can be used outside combat
        if item_or_skill == "Minor Heal":
            return "You used Minor Heal. You feel better!"
        else:
            return f"{item_or_skill} can only be used in combat."
    
    return f"You don't have {item_or_skill}."

def show_shop_items(player: Dict) -> str:
    """Show items available in the shop"""
    shop_items = [
        {"name": "Health Potion", "cost": 50, "description": "Restores health"},
        {"name": "Mana Potion", "cost": 50, "description": "Restores mana"},
        {"name": "Basic Sword", "cost": 100, "description": "+5 attack"},
        {"name": "Wooden Shield", "cost": 80, "description": "+3 defense"},
        {"name": "Skill Book: Fireball", "cost": 200, "description": "Learn Fireball skill"}
    ]
    
    shop_text = "🛒 SHOP ITEMS 🛒\n\n"
    for item in shop_items:
        shop_text += f"- {item['name']} ({item['cost']} gold): {item['description']}\n"
    
    shop_text += f"\nYour gold: {player['gold']}\n"
    shop_text += "To buy an item, type 'buy [item name]'"
    
    return shop_text

def buy_item(parts: List[str], player: Dict, game_state: Dict) -> str:
    """Buy an item from the shop"""
    if len(parts) < 2:
        return "Please specify what to buy. Example: buy [item name]"
    
    item_name = " ".join(parts[1:])
    
    # Simple shop items
    shop_items = {
        "health potion": {"cost": 50, "name": "Health Potion"},
        "mana potion": {"cost": 50, "name": "Mana Potion"},
        "basic sword": {"cost": 100, "name": "Basic Sword"},
        "wooden shield": {"cost": 80, "name": "Wooden Shield"},
        "skill book: fireball": {"cost": 200, "name": "Skill Book: Fireball"}
    }
    
    if item_name.lower() not in shop_items:
        return f"{item_name} is not available in the shop."
    
    item = shop_items[item_name.lower()]
    
    if player["gold"] < item["cost"]:
        return f"You don't have enough gold to buy {item['name']}. You need {item['cost']} gold."
    
    # Process purchase
    player["gold"] -= item["cost"]
    
    # Handle special items like skill books
    if "Skill Book" in item["name"]:
        skill_name = item["name"].split(": ")[1]
        if skill_name not in player["skills"]:
            player["skills"].append(skill_name)
            return f"You learned a new skill: {skill_name}!"
    else:
        player["inventory"].append(item["name"])
    
    return f"You bought {item['name']} for {item['cost']} gold."

def explore_zone(parts: List[str], player: Dict, game_state: Dict) -> str:
    """Explore a zone for random encounters and rewards"""
    if len(parts) < 2:
        return f"Please specify a zone to explore. Available zones: {', '.join(ZONES)}"
    
    zone_name = parts[1].capitalize()
    
    if zone_name not in ZONES:
        return f"Invalid zone. Available zones: {', '.join(ZONES)}"
    
    # Check if player is already in battle
    if player["in_battle"]:
        return "You can't explore while in battle."
    
    # Random encounter
    encounter_type = random.choice(["monster", "treasure", "nothing"])
    
    if encounter_type == "monster":
        # Monster combat would be implemented here
        # For simplicity, just give rewards
        exp_gain = random.randint(10, 30)
        gold_gain = random.randint(5, 15)
        
        player["experience"] += exp_gain
        player["gold"] += gold_gain
        
        # Check for level up
        leveled_up = check_level_up(player)
        level_message = " You leveled up!" if leveled_up else ""
        
        return (
            f"You encountered a monster in the {zone_name}!\n"
            f"After defeating it, you gained {exp_gain} XP and {gold_gain} gold.{level_message}"
        )
    
    elif encounter_type == "treasure":
        gold_gain = random.randint(10, 30)
        player["gold"] += gold_gain
        
        # Random chance to find an item
        if random.random() < 0.3:
            items = ["Health Potion", "Mana Potion", "Mysterious Amulet", "Glowing Herb"]
            found_item = random.choice(items)
            player["inventory"].append(found_item)
            
            return (
                f"You found a treasure chest in the {zone_name}!\n"
                f"Inside was {gold_gain} gold and a {found_item}."
            )
        
        return f"You found a small treasure in the {zone_name}! You gained {gold_gain} gold."
    
    else:
        return f"You explored the {zone_name} but found nothing of interest."

def manage_quests(parts: List[str], player: Dict, game_state: Dict) -> str:
    """Manage player quests"""
    # Simple quest system
    available_quests = [
        {"id": 1, "name": "Herb Gathering", "description": "Collect medicinal herbs", "reward_exp": 100, "reward_gold": 50},
        {"id": 2, "name": "Monster Hunt", "description": "Defeat 5 monsters", "reward_exp": 200, "reward_gold": 100},
        {"id": 3, "name": "Lost Artifact", "description": "Find the ancient artifact", "reward_exp": 300, "reward_gold": 150}
    ]
    
    if len(parts) == 1:
        # List available quests
        quest_text = "📜 AVAILABLE QUESTS 📜\n\n"
        for quest in available_quests:
            quest_text += (
                f"#{quest['id']}: {quest['name']}\n"
                f"- {quest['description']}\n"
                f"- Rewards: {quest['reward_exp']} XP, {quest['reward_gold']} gold\n\n"
            )
        
        quest_text += "To start a quest, type 'quest [id]'"
        return quest_text
    
    # Start specific quest
    try:
        quest_id = int(parts[1])
    except ValueError:
        return "Invalid quest ID. Please enter a number."
    
    # Find quest
    quest = None
    for q in available_quests:
        if q["id"] == quest_id:
            quest = q
            break
    
    if not quest:
        return f"Quest #{quest_id} not found."
    
    # For simplicity, immediately complete the quest
    player["experience"] += quest["reward_exp"]
    player["gold"] += quest["reward_gold"]
    
    # Check for level up
    leveled_up = check_level_up(player)
    level_message = " You leveled up!" if leveled_up else ""
    
    return (
        f"You completed the '{quest['name']}' quest!\n"
        f"You gained {quest['reward_exp']} XP and {quest['reward_gold']} gold.{level_message}"
    )

def show_rank_info(player: Dict) -> str:
    """Show information about player rank and progression"""
    current_rank = player["rank"]
    current_rank_index = RANKS.index(current_rank)
    
    rank_info = (
        f"📊 RANK INFORMATION 📊\n\n"
        f"Your current rank: {current_rank}\n"
        f"Level: {player['level']}\n\n"
    )
    
    # Current rank bonuses
    bonuses = RANK_BONUSES[current_rank]
    rank_info += "Current rank bonuses:\n"
    for bonus, value in bonuses.items():
        if isinstance(value, bool):
            if value:
                rank_info += f"- {bonus} unlocked\n"
        elif isinstance(value, (int, float)):
            if bonus == "max_stats":
                rank_info += f"- Max stats: {value}\n"
            else:
                rank_info += f"- {bonus}: +{int(value * 100)}%\n"
    
    # Next rank information
    if current_rank_index < len(RANKS) - 1:
        next_rank = RANKS[current_rank_index + 1]
        next_level_req = (current_rank_index + 1) * 10
        
        rank_info += f"\nNext rank ({next_rank}) requirements:\n"
        rank_info += f"- Reach level {next_level_req}\n"
        
        # Next rank bonuses
        next_bonuses = RANK_BONUSES[next_rank]
        rank_info += "\nNext rank bonuses:\n"
        for bonus, value in next_bonuses.items():
            if isinstance(value, bool):
                if value:
                    rank_info += f"- {bonus} unlocked\n"
            elif isinstance(value, (int, float)):
                if bonus == "max_stats":
                    rank_info += f"- Max stats: {value}\n"
                else:
                    rank_info += f"- {bonus}: +{int(value * 100)}%\n"
    else:
        rank_info += "\nYou have reached the maximum rank!"
    
    return rank_info
