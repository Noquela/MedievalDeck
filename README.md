# Medieval Deck

A roguelike deckbuilder game built with Pygame featuring AI-generated assets.

## 🎮 Game Overview

Medieval Deck is a turn-based card game where players choose from three heroes (Knight, Mage, Assassin) and battle through procedurally generated encounters. The game features backgrounds and assets generated using Stable Diffusion XL for a unique visual experience.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- RTX 5070 or equivalent GPU (for AI asset generation)
- 8GB+ VRAM recommended

### Installation
```bash
# Clone the repository
git clone https://github.com/Noquela/MedievalDeckClaude.git
cd MedievalDeckClaude

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## 🏗️ Project Structure

```
Medieval-Deck/
├── main.py                 # Main game entry point
├── config.py               # Global constants and settings
├── screens/                # Game state modules
│   ├── menu.py            # Main menu
│   ├── selection.py       # Hero selection
│   ├── gameplay.py        # Combat screen
│   ├── events.py          # Random events
│   └── gameover.py        # End game screen
├── gen_assets/            # AI asset generation
│   └── generate_backgrounds.py
├── cards/                 # Card system
│   ├── deck.py           # Card and deck classes
│   ├── base_cards.json   # Card definitions
│   └── relics.json       # Passive upgrades
├── utils/                 # Shared utilities
│   ├── buttons.py        # UI components
│   ├── transitions.py    # Screen effects
│   └── helpers.py        # Utility functions
├── assets/               # Generated visual assets
│   ├── backgrounds/      # AI-generated backgrounds
│   ├── heroes/          # Character sprites
│   └── ui/              # Interface elements
└── audio/               # Sound effects and music
```

## 🎯 Development Roadmap

The project follows a 15-sprint development cycle:

- **Phase 1 (Sprints 1-4)**: Foundation - Basic structure, menu system, hero selection, AI integration
- **Phase 2 (Sprints 5-8)**: Core Mechanics - Combat system, turn management, cards, enemy AI
- **Phase 3 (Sprints 9-12)**: Progression - Win/lose conditions, events, shop, relics
- **Phase 4 (Sprints 13-15)**: Polish - Complete progression, animations, MVP finalization

## 🤖 AI Asset Generation

The game uses Stable Diffusion XL to generate unique backgrounds for each hero and combat scenario. Assets are cached to avoid regeneration and use a fixed seed for consistency.

```bash
# Generate all hero backgrounds
python gen_assets/generate_backgrounds.py
```

## 🎮 Game Features

- **Three Unique Heroes**: Knight (defensive), Mage (magical), Assassin (balanced)
- **Turn-Based Combat**: Strategic card-based battles
- **Procedural Generation**: Random events and encounters
- **AI-Generated Visuals**: Unique backgrounds for each scenario
- **Progression System**: Cards, relics, and upgrades
- **Roguelike Elements**: Permanent progression with run-based gameplay

## 🛠️ Technical Details

- **Engine**: Pygame 2.5+
- **AI Generation**: Diffusers + Stable Diffusion XL
- **Resolution**: 1280x720
- **Target Platform**: Windows (with plans for cross-platform)

## 📝 Contributing

This project follows a structured sprint-based development approach. See `CLAUDE.md` for detailed development guidelines and architectural decisions.

## 📄 License

This project is developed as part of a game development learning exercise.