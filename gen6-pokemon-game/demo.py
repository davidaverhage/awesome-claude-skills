#!/usr/bin/env python3
"""
Demo script to showcase the Gen VI Pokemon Game features
Run this to see all modules in action
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def demo_data_loading():
    """Demonstrate data loading"""
    print_header("1. DATA LOADING DEMO")
    
    import json
    
    # Load Pokemon data
    with open("pokemon/base_stats.json", 'r') as f:
        pokemon_data = json.load(f)["pokemon"]
    
    print(f"✓ Loaded {len(pokemon_data)} Pokemon species")
    print("\nSample Pokemon:")
    for i, p in enumerate(pokemon_data[:3], 1):
        types = f"{p['type1']}/{p['type2']}" if p['type2'] else p['type1']
        print(f"  {i}. {p['name']} - Type: {types}")
        print(f"     Base Stats: HP={p['base_stats']['hp']}, ATK={p['base_stats']['attack']}, DEF={p['base_stats']['defense']}")
    
    # Load moves
    with open("moves/move_data.json", 'r') as f:
        move_data = json.load(f)["moves"]
    
    print(f"\n✓ Loaded {len(move_data)} moves")
    print("\nSample Moves:")
    for i, m in enumerate(move_data[:3], 1):
        print(f"  {i}. {m['name']} - Type: {m['type']}, Power: {m['power']}, Accuracy: {m['accuracy']}%")
    
    # Load maps
    with open("overworld/maps/map_headers.json", 'r') as f:
        map_data = json.load(f)["maps"]
    
    print(f"\n✓ Loaded {len(map_data)} maps")
    print("\nSample Maps:")
    for i, m in enumerate(map_data[:3], 1):
        print(f"  {i}. {m['name']} - Type: {m['type']}, Size: {m['width']}x{m['height']}")


def demo_battle_engine():
    """Demonstrate battle engine"""
    print_header("2. BATTLE ENGINE DEMO")
    
    from battle.battle_engine import BattleEngine
    
    # Create Pokemon
    pikachu = {
        "name": "Pikachu",
        "level": 25,
        "type1": "Electric",
        "type2": None,
        "stats": {
            "hp": 80,
            "attack": 55,
            "defense": 40,
            "special_attack": 50,
            "special_defense": 50,
            "speed": 90
        },
        "current_hp": 80,
        "status": None
    }
    
    charmander = {
        "name": "Charmander",
        "level": 25,
        "type1": "Fire",
        "type2": None,
        "stats": {
            "hp": 78,
            "attack": 52,
            "defense": 43,
            "special_attack": 60,
            "special_defense": 50,
            "speed": 65
        },
        "current_hp": 78,
        "status": None
    }
    
    engine = BattleEngine()
    
    print(f"Battle: {pikachu['name']} vs {charmander['name']}")
    print(f"  {pikachu['name']}: {pikachu['current_hp']}/{pikachu['stats']['hp']} HP")
    print(f"  {charmander['name']}: {charmander['current_hp']}/{charmander['stats']['hp']} HP")
    
    # Execute turn
    print(f"\nTurn 1:")
    player_dmg, opponent_dmg = engine.execute_turn(
        pikachu, "Thunder Shock",
        charmander, "Ember"
    )
    
    print(f"\nResults:")
    print(f"  {pikachu['name']}: {pikachu['current_hp']}/{pikachu['stats']['hp']} HP")
    print(f"  {charmander['name']}: {charmander['current_hp']}/{charmander['stats']['hp']} HP")


def demo_battle_ai():
    """Demonstrate battle AI"""
    print_header("3. BATTLE AI DEMO")
    
    from battle.battle_ai import BattleAI
    
    # Create test Pokemon
    bulbasaur = {
        "name": "Bulbasaur",
        "type1": "Grass",
        "type2": "Poison",
        "stats": {"hp": 85, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45},
        "current_hp": 85
    }
    
    squirtle = {
        "name": "Squirtle",
        "type1": "Water",
        "type2": None,
        "stats": {"hp": 90, "attack": 48, "defense": 65, "special_attack": 50, "special_defense": 64, "speed": 43},
        "current_hp": 90
    }
    
    # Test AI at different difficulty levels
    for difficulty in ["easy", "normal", "hard"]:
        ai = BattleAI(difficulty=difficulty)
        available_moves = ["Vine Whip", "Tackle", "Growl", "Leech Seed"]
        
        print(f"\nAI Difficulty: {difficulty.upper()}")
        print(f"  Available moves: {', '.join(available_moves)}")
        print(f"  Matchup: {bulbasaur['name']} (Grass/Poison) vs {squirtle['name']} (Water)")
        
        selected_move = ai.select_move(bulbasaur, squirtle, available_moves)
        print(f"  → Selected: {selected_move}")


def demo_event_system():
    """Demonstrate event scripting"""
    print_header("4. EVENT SCRIPTING DEMO")
    
    import yaml
    
    # Load event scripts
    with open("scripts/event_scripts.yaml", 'r') as f:
        events = yaml.safe_load(f)
    
    print(f"✓ Loaded {len(events['events'])} event scripts")
    
    # Show sample events
    print("\nSample Events:")
    for i, event in enumerate(events['events'][:3], 1):
        print(f"\n  {i}. {event['name']} (Type: {event['type']})")
        print(f"     Trigger: {event['trigger']}")
        if 'script' in event and len(event['script']) > 0:
            first_action = event['script'][0]
            print(f"     First action: {first_action.get('action', 'N/A')}")


def demo_ui_system():
    """Demonstrate UI system"""
    print_header("5. UI SYSTEM DEMO")
    
    import json
    
    with open("ui/menus.json", 'r') as f:
        menus = json.load(f)
    
    print(f"✓ Loaded {len(menus['menus'])} menu interfaces")
    
    print("\nAvailable Menus:")
    for i, (menu_id, menu) in enumerate(menus['menus'].items(), 1):
        print(f"  {i}. {menu['title'] or menu_id} - Type: {menu['type']}")
    
    # Show main menu details
    main_menu = menus['menus']['main_menu']
    print(f"\nMain Menu Items:")
    for item in main_menu['items']:
        status = "✓" if item['enabled'] else "✗"
        print(f"  {status} {item['label']}")


def demo_save_system():
    """Demonstrate save system"""
    print_header("6. SAVE SYSTEM DEMO")
    
    import json
    
    with open("save/save_structure.json", 'r') as f:
        save_format = json.load(f)
    
    print(f"✓ Save format version: {save_format['save_format_version']}")
    print(f"✓ Structure sections: {len(save_format['structure'])}")
    
    print("\nSave File Sections:")
    for section, details in save_format['structure'].items():
        if isinstance(details, dict):
            print(f"  • {section}")


def main():
    """Run all demos"""
    print("\n" + "*"*60)
    print("*" + " "*18 + "GEN VI POKEMON GAME" + " "*19 + "*")
    print("*" + " "*20 + "DEMO SHOWCASE" + " "*23 + "*")
    print("*"*60)
    
    try:
        demo_data_loading()
        demo_battle_engine()
        demo_battle_ai()
        demo_event_system()
        demo_ui_system()
        demo_save_system()
        
        print_header("DEMO COMPLETE")
        print("✓ All modules loaded and tested successfully!")
        print("✓ Ready for platform conversion")
        print("\nNext steps:")
        print("  1. Run 'python main/game_loop.py' to start the game")
        print("  2. Test individual modules in their respective directories")
        print("  3. Replace asset placeholders with actual graphics/audio")
        print("  4. Convert to target platform (Unity, Godot, PS Vita, Web)")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
