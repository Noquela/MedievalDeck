"""
Global configuration constants for Medieval Deck game.
"""

# Screen settings - Ultrawide 3440x1440
SCREEN_WIDTH = 3440
SCREEN_HEIGHT = 1440
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Game settings
INITIAL_HEALTH = 100
INITIAL_MANA = 3
MAX_HAND_SIZE = 7
CARDS_PER_TURN = 1

# File paths
ASSETS_DIR = "assets"
BACKGROUNDS_DIR = f"{ASSETS_DIR}/backgrounds"
HEROES_DIR = f"{ASSETS_DIR}/heroes"
UI_DIR = f"{ASSETS_DIR}/ui"
AUDIO_DIR = "audio"
CARDS_DIR = "cards"

# AI Generation settings - Ultrawide resolution
AI_SEED = 42
AI_IMAGE_SIZE = (3440, 1440)
AI_BATCH_SIZE = 1

# Heroes
HEROES = {
    "knight": {
        "name": "Knight",
        "health": 120,
        "mana": 2,
        "description": "A sturdy warrior with high health and defensive abilities"
    },
    "mage": {
        "name": "Mage", 
        "health": 80,
        "mana": 4,
        "description": "A powerful spellcaster with high mana and magical abilities"
    },
    "assassin": {
        "name": "Assassin",
        "health": 90,
        "mana": 3,
        "description": "A swift fighter with balanced stats and critical strikes"
    }
}