---
name: gen6-pokemon-game
description: A modular Pokémon game reconstruction based on Generation VI style. This skill provides a complete disassembly and reformat of the Pokémon Crystal ROM, reorganized into source-code style modules compatible with modern development environments.
---

# Gen VI Pokémon Game Reconstruction

This skill provides a fully modular Pokémon game engine based on Generation VI mechanics, reorganized from a complete disassembly of Pokémon Crystal ROM into modern Python source code modules.

## Overview

This project reconstructs a fully working Pokémon game with:
- Turn-based battle system with Gen VI mechanics
- Overworld navigation and map system
- Dynamic event scripting engine
- Complete Pokémon data (stats, moves, evolutions)
- Save/load system
- Menu and UI framework

All components are modular and ready for conversion into a working game on platforms like PS Vita, Unity, Godot, or Python-based engines.

## Project Structure

```
gen6-pokemon-game/
├── main/
│   └── game_loop.py           # Main game loop and initialization
├── pokemon/
│   ├── base_stats.json        # Pokémon base statistics
│   └── evolution_learnsets.json  # Evolution chains and learnable moves
├── moves/
│   └── move_data.json         # Move database with effects
├── battle/
│   ├── battle_engine.py       # Turn-based battle mechanics
│   └── battle_ai.py           # AI opponent logic
├── overworld/
│   └── maps/
│       └── map_headers.json   # Map metadata and connections
├── assets/
│   └── tilesets/
│       └── johto_town_tileset.meta  # Tileset definitions
├── scripts/
│   ├── pointer_table.yaml     # Script pointer mappings
│   └── event_scripts.yaml     # Dynamic event definitions
├── ui/
│   └── menus.json            # Menu configurations
└── save/
    ├── save_structure.json   # Save file format
    └── README.md             # Save system documentation
```

## Getting Started

### Running the Game

```bash
cd gen6-pokemon-game
python main/game_loop.py
```

### Dependencies

```bash
pip install pygame  # For graphics and input
pip install pyyaml  # For YAML parsing
```

## Module Documentation

### Main Game Loop

The `main/game_loop.py` module handles:
- Game initialization
- Main update/render loop
- State management (overworld, battle, menu)
- Event processing

### Pokémon System

Data files in the `pokemon/` directory define:
- **base_stats.json**: HP, Attack, Defense, Speed, Special Attack, Special Defense, Type(s), Abilities
- **evolution_learnsets.json**: Evolution conditions, level-up moves, TM/HM compatibility

### Battle Engine

The battle system (`battle/`) implements:
- Turn-based combat with Gen VI mechanics
- Move effects and damage calculation
- Status conditions and weather
- AI decision-making for NPC trainers

### Overworld System

The overworld (`overworld/maps/`) provides:
- Map loading and rendering
- Collision detection
- NPC and trainer interactions
- Map connections and transitions

### Event Scripting

The scripting system (`scripts/`) enables:
- Dynamic NPC dialogues
- Item acquisition
- Story progression triggers
- Conditional event execution

### UI System

The UI framework (`ui/`) handles:
- Menu navigation
- Item/Pokémon management screens
- Battle interface
- Dialogue boxes

### Save System

The save system (`save/`) implements:
- Player progress serialization
- Pokémon party and box storage
- Item inventory
- Game flags and variables

## Usage Instructions

### Adding New Pokémon

1. Edit `pokemon/base_stats.json` to add base statistics
2. Edit `pokemon/evolution_learnsets.json` to define evolution conditions and moves
3. Sprites should be placed in `assets/pokemon/` (stubs provided)

### Creating New Maps

1. Define map headers in `overworld/maps/map_headers.json`
2. Create corresponding tileset metadata in `assets/tilesets/`
3. Link map connections in the map header

### Adding Event Scripts

1. Add script definitions to `scripts/event_scripts.yaml`
2. Update `scripts/pointer_table.yaml` to map script IDs to locations
3. Events will trigger when player interacts with designated tiles

## Platform Conversion

### For Unity/Godot

- Use JSON/YAML data files directly with built-in parsers
- Port Python logic to C# (Unity) or GDScript (Godot)
- Replace pygame rendering with engine-specific rendering

### For PS Vita

- Use vitaGL or similar library for rendering
- Adapt input handling for Vita controls
- Optimize asset loading for handheld performance

### For Web (JavaScript)

- Convert Python battle engine to JavaScript
- Use Phaser.js or similar framework
- Load JSON data with fetch API

## Placeholder Notes

Graphics, music, and tiles use stubs/placeholders where needed. Replace with:
- Pokémon sprites: 96x96 PNG files
- Map tiles: 16x16 tileset images
- Sound effects: OGG or MP3 format
- Music: Looping OGG or MP3 tracks

## Development Tips

1. Start by running `game_loop.py` to verify the framework
2. Test battle engine independently with `battle/battle_engine.py`
3. Use save/load frequently during testing
4. Placeholder graphics allow functional testing without assets

## License

This is a disassembly/reconstruction project for educational purposes. Original Pokémon content is owned by Nintendo, Game Freak, and The Pokémon Company.
