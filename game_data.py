"""
Game data and constants for the RPG WhatsApp Bot
This module contains game mechanics information, items, skills, and other data
"""

# Race data with traits
RACES = {
    "Human": {
        "description": "Versatile and adaptable",
        "bonuses": {"exp_gain": 0.05},
        "penalties": {}
    },
    "Elf": {
        "description": "Swift and agile",
        "bonuses": {"dodge": 0.10},
        "penalties": {"endurance": -0.05}
    },
    "Dwarf": {
        "description": "Stout and strong",
        "bonuses": {"defense": 0.15},
        "penalties": {"speed": -0.10}
    },
    "Orc": {
        "description": "Brutal and powerful",
        "bonuses": {"melee_damage": 0.20},
        "penalties": {"intelligence": -0.10}
    },
    "Anaon": {
        "description": "Ethereal wraith with control over dark energies",
        "bonuses": {"dark_magic": 0.15},
        "penalties": {"max_hp": -0.10}
    }
}

# Class data with bonuses
CLASSES = {
    "Warrior": {
        "description": "Master of weapons and physical combat",
        "bonuses": {"melee_damage": 0.15, "endurance": 10},
        "starting_items": ["Iron Axe", "Steel Shield"]
    },
    "Archer": {
        "description": "Skilled in ranged combat",
        "bonuses": {"range_damage": 0.15, "agility": 10},
        "starting_items": ["Wooden Bow", "Quiver of 20 Arrows"]
    },
    "Mage": {
        "description": "Wielder of arcane magic",
        "bonuses": {"magic_power": 0.20, "intelligence": 10},
        "starting_items": ["Carved Wooden Staff", "Basic Spellbook"]
    },
    "Paladin": {
        "description": "Holy warrior with defensive and healing abilities",
        "bonuses": {"defense": 0.10, "healing": 0.05, "endurance": 10},
        "starting_items": ["Blessed Shortsword", "Major Healing Potion"]
    },
    "Rogue": {
        "description": "Stealthy and agile fighter",
        "bonuses": {"dodge": 0.20, "crit": 0.20, "agility": 10},
        "starting_items": ["Light Dagger", "Shadow Cloak"]
    },
    "Druid": {
        "description": "Nature magic user with healing abilities",
        "bonuses": {"healing": 0.15, "nature_control": 0.15, "intelligence": 5, "strength": 5},
        "starting_items": ["Sacred Branch", "5x Healing Herbs"]
    },
    "Necromancer": {
        "description": "Master of death magic and summoning undead",
        "bonuses": {"summon": 0.15, "life_leech": 0.10, "dark_magic": 10},
        "starting_items": ["Rat Skull", "Tome of Necromancy"]
    },
    "Bard": {
        "description": "Magical musician with support abilities",
        "bonuses": {"support": 0.20, "party_buffs": 0.15, "charisma": 10, "agility": 5},
        "starting_items": ["Lute", "Enchanted Flute"]
    },
    "Berserker": {
        "description": "Rage-fueled warrior with high damage",
        "bonuses": {"rage": 0.25, "strength": 10, "endurance": 10},
        "penalties": {"defense": -0.15},
        "starting_items": ["Rusty Hatchet", "Rage Flask"]
    },
    "Alchemist": {
        "description": "Creator of potions and bombs",
        "bonuses": {"potions": 0.20, "bombs": 0.15, "intelligence": 10, "constitution": 5},
        "starting_items": ["Basic Alchemy Kit", "3x Smoke Bombs"]
    },
    "Guardian": {
        "description": "Protective warrior focused on defense",
        "bonuses": {"ally_protection": 0.20, "magic_barriers": 0.15, "defense": 10, "endurance": 10},
        "starting_items": ["Guard's Hammer", "Magic Barrier Scroll"]
    },
    "Scout": {
        "description": "Expert in reconnaissance and traps",
        "bonuses": {"reconnaissance": 0.20, "traps": 0.15, "agility": 10, "intelligence": 5},
        "starting_items": ["Spyglass", "2x Mechanical Traps"]
    },
    "Chronomancer": {
        "description": "Manipulator of time and space",
        "bonuses": {"time_manipulation": 0.20, "magic": 0.15, "intelligence": 10},
        "starting_items": ["Mystic Hourglass", "Enchanted Pocket Watch"]
    },
    "Artisan": {
        "description": "Master crafter of weapons and armor",
        "bonuses": {"crafting": 0.25, "upgrade": 0.20, "commerce": 10, "constitution": 5},
        "starting_items": ["Portable Anvil", "Blacksmith's Hammer"]
    }
}

# Elements data with advantage/disadvantage
ELEMENTS = {
    "Fire": {
        "description": "Destructive burning element",
        "advantage": "Plant",
        "disadvantage": "Water"
    },
    "Water": {
        "description": "Flowing liquid element",
        "advantage": "Fire",
        "disadvantage": "Plant"
    },
    "Plant": {
        "description": "Living growth element",
        "advantage": "Water",
        "disadvantage": "Fire"
    },
    "Earth": {
        "description": "Solid ground element",
        "advantage": "Wind",
        "disadvantage": "Water"
    },
    "Wind": {
        "description": "Moving air element",
        "advantage": "Earth",
        "disadvantage": "Fire"
    },
    "Darkness": {
        "description": "Shadowy void element",
        "advantage": "Light",
        "disadvantage": None
    },
    "Light": {
        "description": "Radiant illumination element",
        "advantage": "Darkness",
        "disadvantage": None
    }
}

# Zone data with effects
ZONES = {
    "Forest": {
        "description": "Dense woodland with abundant plant life",
        "bonuses": {"Plant": {"damage": 0.10}},
        "penalties": {"Fire": {"defense": -0.10}}
    },
    "Volcano": {
        "description": "Fiery mountain with rivers of lava",
        "bonuses": {"Fire": {"attack_speed": 0.15}},
        "penalties": {"Water": {"resistance": -0.15}}
    },
    "Ocean": {
        "description": "Vast expanse of water and waves",
        "bonuses": {"Water": {"max_hp": 0.10}},
        "penalties": {"Plant": {"dodge": -0.10}}
    },
    "Mountain": {
        "description": "Rocky highlands reaching to the skies",
        "bonuses": {"Earth": {"endurance": 0.10}},
        "penalties": {"Wind": {"agility": -0.10}}
    },
    "Sky": {
        "description": "Open air high above the ground",
        "bonuses": {"Wind": {"dodge": 0.12}},
        "penalties": {"Earth": {"accuracy": -0.12}}
    }
}

# Rank data with level requirements and bonuses
RANKS = {
    "G": {
        "level_min": 1,
        "level_max": 9,
        "max_stats": 100,
        "bonuses": {"exp_gain": 0.05}
    },
    "F": {
        "level_min": 10,
        "level_max": 19,
        "max_stats": 150,
        "bonuses": {"gold_gain": 0.05}
    },
    "E": {
        "level_min": 20,
        "level_max": 29,
        "max_stats": 200,
        "bonuses": {"karma_gain": 0.05}
    },
    "D": {
        "level_min": 30,
        "level_max": 39,
        "max_stats": 250,
        "bonuses": {"exp_gain": 0.10}
    },
    "C": {
        "level_min": 40,
        "level_max": 49,
        "max_stats": 300,
        "bonuses": {"gold_gain": 0.10}
    },
    "B": {
        "level_min": 50,
        "level_max": 59,
        "max_stats": 350,
        "bonuses": {"karma_gain": 0.10}
    },
    "A": {
        "level_min": 60,
        "level_max": 69,
        "max_stats": 400,
        "bonuses": {"exp_gain": 0.15},
        "unlocks": ["summons"]
    },
    "S": {
        "level_min": 70,
        "level_max": 79,
        "max_stats": 450,
        "bonuses": {"gold_gain": 0.15},
        "unlocks": ["ascensions"]
    },
    "SS": {
        "level_min": 80,
        "level_max": 999,
        "max_stats": 500,
        "bonuses": {"karma_gain": 0.20},
        "unlocks": ["divine_raids"]
    }
}

# Skills data
SKILLS = {
    "Punch": {
        "description": "Basic melee attack",
        "damage_type": "physical",
        "base_damage": 5,
        "attribute": "strength",
        "cooldown": 0
    },
    "Mind Shuffle": {
        "description": "Confuse target with mental attack",
        "damage_type": "magic",
        "base_damage": 8,
        "attribute": "intelligence",
        "cooldown": 2
    },
    "Precision Shot": {
        "description": "Accurate ranged attack",
        "damage_type": "physical",
        "base_damage": 7,
        "attribute": "agility",
        "cooldown": 1
    },
    "Minor Heal": {
        "description": "Recover a small amount of health",
        "effect_type": "healing",
        "base_amount": 10,
        "attribute": "intelligence",
        "cooldown": 3
    },
    "Magic Shield": {
        "description": "Create protective barrier",
        "effect_type": "defense",
        "base_amount": 15,
        "attribute": "intelligence",
        "duration": 3,
        "cooldown": 4
    },
    "Fireball": {
        "description": "Launch a ball of fire",
        "damage_type": "fire",
        "base_damage": 15,
        "attribute": "intelligence",
        "cooldown": 3
    }
}

# Shop items
SHOP_ITEMS = {
    "Health Potion": {
        "description": "Restores 50 health",
        "cost": 50,
        "type": "consumable",
        "effect": {"health": 50}
    },
    "Mana Potion": {
        "description": "Restores 50 mana",
        "cost": 50,
        "type": "consumable",
        "effect": {"mana": 50}
    },
    "Basic Sword": {
        "description": "Simple sword with +5 attack",
        "cost": 100,
        "type": "weapon",
        "attributes": {"attack": 5}
    },
    "Wooden Shield": {
        "description": "Simple shield with +3 defense",
        "cost": 80,
        "type": "armor",
        "attributes": {"defense": 3}
    },
    "Skill Book: Fireball": {
        "description": "Learn the Fireball skill",
        "cost": 200,
        "type": "skill_book",
        "teaches": "Fireball"
    }
}

# Quest data
QUESTS = [
    {
        "id": 1,
        "name": "Herb Gathering",
        "description": "Collect medicinal herbs from the Forest",
        "level_req": 1,
        "zone": "Forest",
        "rewards": {
            "exp": 100,
            "gold": 50,
            "items": ["Health Potion"]
        }
    },
    {
        "id": 2,
        "name": "Monster Hunt",
        "description": "Defeat 5 monsters in the Volcano",
        "level_req": 5,
        "zone": "Volcano",
        "rewards": {
            "exp": 200,
            "gold": 100,
            "karma": 10
        }
    },
    {
        "id": 3,
        "name": "Lost Artifact",
        "description": "Find the ancient artifact hidden in the Ocean depths",
        "level_req": 10,
        "zone": "Ocean",
        "rewards": {
            "exp": 300,
            "gold": 150,
            "karma": 20,
            "items": ["Skill Book: Water Blast"]
        }
    }
]
