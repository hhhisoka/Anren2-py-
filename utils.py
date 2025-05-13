import os
import json
import logging
from typing import Dict, Any

# Initialize logging
logger = logging.getLogger(__name__)

# Game state file
GAME_STATE_FILE = "game_state.json"

def save_game_state(game_state: Dict[str, Any]) -> bool:
    """Save the game state to a JSON file"""
    try:
        with open(GAME_STATE_FILE, 'w') as f:
            json.dump(game_state, f, indent=2)
        logger.info("Game state saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving game state: {e}")
        return False

def load_game_state() -> Dict[str, Any]:
    """Load game state from JSON file or create a new one"""
    try:
        if os.path.exists(GAME_STATE_FILE):
            with open(GAME_STATE_FILE, 'r') as f:
                game_state = json.load(f)
            logger.info("Game state loaded successfully")
            return game_state
        else:
            logger.info("No game state file found, creating new")
            game_state = {
                "players": {},
                "active_battles": {},
                "zones": {
                    "Forest": {"element_bonus": "Plant", "element_penalty": "Fire"},
                    "Volcano": {"element_bonus": "Fire", "element_penalty": "Water"},
                    "Ocean": {"element_bonus": "Water", "element_penalty": "Plant"},
                    "Mountain": {"element_bonus": "Earth", "element_penalty": "Wind"},
                    "Sky": {"element_bonus": "Wind", "element_penalty": "Earth"}
                },
                "items": {},
                "deities": {}
            }
            save_game_state(game_state)
            return game_state
    except Exception as e:
        logger.error(f"Error loading game state: {e}")
        # Return a new game state
        return {
            "players": {},
            "active_battles": {},
            "zones": {
                "Forest": {"element_bonus": "Plant", "element_penalty": "Fire"},
                "Volcano": {"element_bonus": "Fire", "element_penalty": "Water"},
                "Ocean": {"element_bonus": "Water", "element_penalty": "Plant"},
                "Mountain": {"element_bonus": "Earth", "element_penalty": "Wind"},
                "Sky": {"element_bonus": "Wind", "element_penalty": "Earth"}
            },
            "items": {},
            "deities": {}
        }
