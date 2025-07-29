# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Medieval Deck is a roguelike deckbuilder game built with Pygame, featuring AI-generated assets using Stable Diffusion XL. The project follows a 15-sprint development roadmap with clear architectural separation between game systems.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py

# Generate AI assets (requires RTX 5070 or similar GPU)
python gen_assets/generate_backgrounds.py

# Run tests (all test files are in /tests/ directory)
python tests/test_sprint1.py
python tests/test_sprint2.py
```

### Sprint Development Rules
```bash
# After completing each sprint, automatically run:
git add .
git commit -m "Final da Sprint X: [description]"
git push origin main
```

### Technical Specifications
- **Resolution**: 3440x1440 (ultrawide) for all backgrounds, UI and images
- **Repository**: https://github.com/Noquela/MedievalDeckClaude
- **AI Assets**: Store in `gen_assets/` with specific subfolders by type
- **Testing**: All test files go in `/tests/` directory

### Asset Generation
```bash
# Generate backgrounds for all heroes
python -c "from gen_assets.generate_backgrounds import AssetGenerator; AssetGenerator().generate_all_backgrounds()"

# Generate specific hero background
python -c "from gen_assets.generate_backgrounds import AssetGenerator; AssetGenerator().generate_background('knight')"
```

## Architecture Overview

### Core Game Loop Structure
The game uses a state-based architecture with the main loop in `main.py` managing different game states:
- **MENU**: Initial screen with navigation options
- **SELECTION**: Hero selection with AI-generated backgrounds
- **GAMEPLAY**: Turn-based combat with card mechanics
- **EVENTS**: Random events between combats
- **GAMEOVER**: End screen with restart options

### Module Organization

#### `/screens/` - Game State Modules
Each screen module handles a specific game state with consistent interface:
- `menu.py` - Main menu with title and navigation buttons
- `selection.py` - Hero selection with dynamic backgrounds
- `gameplay.py` - Combat interface with turn management
- `events.py` - Random event system between combats
- `gameover.py` - End game screen with results

#### `/cards/` - Card System
- `deck.py` - Core Card and Deck classes with mana costs and effects
- `base_cards.json` - Card definitions (attack, defense, magic types)
- `relics.json` - Passive upgrade items with permanent effects

#### `/gen_assets/` - AI Asset Pipeline
- `generate_backgrounds.py` - SDXL integration with hero-specific prompts
- Uses fixed seed (42) for reproducible generation
- Caches generated assets to avoid regeneration
- Optimized for RTX 5070 with specific batch settings

#### `/utils/` - Shared Components
- `buttons.py` - Reusable UI button system with hover states
- `transitions.py` - Screen transition effects
- `helpers.py` - Common utility functions

### Key Design Patterns

#### Hero System
Heroes are defined in `config.py` with structured data including health, mana, and descriptions. The selection system dynamically loads AI-generated backgrounds based on hero choice.

#### Turn-Based Combat
Combat alternates between player and enemy turns with distinct phases:
1. Draw cards phase
2. Action selection phase  
3. Effect resolution phase
4. End turn cleanup

#### Asset Generation Integration
AI asset generation is separated from game logic with caching mechanisms. Generated assets are stored in `/assets/` with consistent naming conventions.

#### Modular Screen Architecture
Each screen module follows the same interface pattern with `render()` and `handle_events()` methods, making state transitions predictable.

## Sprint Development Rules

### Code Organization Rules
1. Never rewrite files in `/gen_assets/` - these contain AI generation logic
2. Always modularize by screen or system - don't mix gameplay logic across modules
3. Preserve the defined file structure and naming conventions
4. Use docstrings for all functions following the established pattern

### Asset Management Rules
1. Never overwrite existing generated images - check for existence first
2. Use the fixed seed (42) for reproducible AI generation
3. Store all generated assets in appropriate `/assets/` subdirectories
4. Cache AI generation results to avoid unnecessary regeneration

### Development Workflow
The project follows a sprint-based development cycle:
- **Sprints 1-4**: Foundation (structure, menu, selection, AI integration)
- **Sprints 5-8**: Core mechanics (combat, turns, cards, enemy AI)
- **Sprints 9-12**: Progression (win/lose, events, shop, relics)
- **Sprints 13-15**: Polish (progression, animations, MVP completion)

Each sprint builds incrementally on previous work without breaking existing functionality.

## Technical Dependencies

### Required Hardware
- RTX 5070 or equivalent GPU with 8GB+ VRAM for AI generation
- Python 3.8+ environment

### Key Libraries
- `pygame>=2.5.0` for game engine
- `diffusers>=0.21.0` for Stable Diffusion XL
- `torch>=2.0.0` for AI model execution

### Development Environment
Project is designed for deployment to: https://github.com/Noquela/MedievalDeckClaude