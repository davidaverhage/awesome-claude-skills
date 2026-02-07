#!/usr/bin/env python3
"""
Battle Engine for Gen VI Pokémon Game
Implements turn-based battle mechanics with damage calculation, status effects, and battle flow.
"""

import json
import os
import random
import math


class BattleEngine:
    """Core battle system implementing Gen VI mechanics"""
    
    # Type effectiveness chart (simplified)
    TYPE_CHART = {
        "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
        "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
        "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
        "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
        "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
        "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
        "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
        "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
        "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
        "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
        "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
        "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
        "Rock": {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
        "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
        "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
        "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
        "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
        "Fairy": {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2, "Dark": 2, "Steel": 0.5}
    }
    
    def __init__(self):
        """Initialize battle engine"""
        self.move_data = {}
        self.load_move_data()
    
    def load_move_data(self):
        """Load move data from JSON file"""
        try:
            moves_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "moves",
                "move_data.json"
            )
            with open(moves_path, 'r') as f:
                data = json.load(f)
                self.move_data = {move["name"]: move for move in data["moves"]}
        except FileNotFoundError:
            print("Warning: move_data.json not found")
    
    def calculate_damage(self, attacker, defender, move_name, weather=None):
        """
        Calculate damage using Gen VI damage formula
        
        Damage = ((2 * Level / 5 + 2) * Power * A/D) / 50 + 2
        Then apply modifiers for STAB, type effectiveness, critical hits, etc.
        """
        if move_name not in self.move_data:
            return 0
        
        move = self.move_data[move_name]
        
        # Status moves don't deal damage
        if move["category"] == "Status":
            return 0
        
        power = move["power"]
        if power == 0:
            return 0
        
        level = attacker.get("level", 50)
        
        # Determine attack and defense stats
        if move["category"] == "Physical":
            attack = attacker["stats"]["attack"]
            defense = defender["stats"]["defense"]
        else:  # Special
            attack = attacker["stats"]["special_attack"]
            defense = defender["stats"]["special_defense"]
        
        # Base damage calculation
        damage = ((2 * level / 5 + 2) * power * attack / defense) / 50 + 2
        
        # STAB (Same Type Attack Bonus)
        attacker_type1 = attacker.get("type1")
        attacker_type2 = attacker.get("type2")
        move_type = move["type"]
        
        if move_type == attacker_type1 or move_type == attacker_type2:
            damage *= 1.5
        
        # Type effectiveness
        defender_type1 = defender.get("type1")
        defender_type2 = defender.get("type2")
        
        effectiveness = self.get_type_effectiveness(move_type, defender_type1)
        if defender_type2:
            effectiveness *= self.get_type_effectiveness(move_type, defender_type2)
        
        damage *= effectiveness
        
        # Critical hit (6.25% chance in Gen VI)
        if random.random() < 0.0625:
            damage *= 1.5
            print("Critical hit!")
        
        # Random factor (0.85 to 1.0)
        damage *= random.uniform(0.85, 1.0)
        
        return int(damage)
    
    def get_type_effectiveness(self, attack_type, defender_type):
        """Get type effectiveness multiplier"""
        if attack_type in self.TYPE_CHART:
            return self.TYPE_CHART[attack_type].get(defender_type, 1.0)
        return 1.0
    
    def apply_status_effect(self, pokemon, status):
        """Apply a status condition to a Pokémon"""
        if pokemon.get("status") is not None:
            return False  # Already has a status
        
        pokemon["status"] = status
        return True
    
    def process_status_damage(self, pokemon):
        """Process damage from status conditions at end of turn"""
        status = pokemon.get("status")
        if not status:
            return 0
        
        max_hp = pokemon["stats"]["hp"]
        
        if status == "burn":
            damage = max_hp // 16
            print(f"{pokemon['name']} is hurt by its burn!")
            return damage
        elif status == "poison":
            damage = max_hp // 8
            print(f"{pokemon['name']} is hurt by poison!")
            return damage
        
        return 0
    
    def check_speed(self, pokemon1, pokemon2, move1, move2):
        """
        Determine which Pokémon moves first
        Returns True if pokemon1 goes first, False otherwise
        """
        # Check move priority
        priority1 = self.move_data.get(move1, {}).get("priority", 0)
        priority2 = self.move_data.get(move2, {}).get("priority", 0)
        
        if priority1 > priority2:
            return True
        elif priority2 > priority1:
            return False
        
        # Same priority - check speed stat
        speed1 = pokemon1["stats"]["speed"]
        speed2 = pokemon2["stats"]["speed"]
        
        if speed1 > speed2:
            return True
        elif speed2 > speed1:
            return False
        else:
            # Speed tie - random
            return random.choice([True, False])
    
    def execute_turn(self, player_pokemon, player_move, opponent_pokemon, opponent_move):
        """
        Execute a full battle turn with both Pokémon's moves
        Returns tuple: (player_damage_dealt, opponent_damage_dealt)
        """
        print(f"\n--- Turn Execution ---")
        
        # Determine move order
        player_first = self.check_speed(
            player_pokemon, opponent_pokemon,
            player_move, opponent_move
        )
        
        if player_first:
            first_attacker = player_pokemon
            first_move = player_move
            first_defender = opponent_pokemon
            second_attacker = opponent_pokemon
            second_move = opponent_move
            second_defender = player_pokemon
        else:
            first_attacker = opponent_pokemon
            first_move = opponent_move
            first_defender = player_pokemon
            second_attacker = player_pokemon
            second_move = player_move
            second_defender = opponent_pokemon
        
        # First attack
        print(f"{first_attacker['name']} used {first_move}!")
        damage1 = self.calculate_damage(first_attacker, first_defender, first_move)
        
        if damage1 > 0:
            first_defender["current_hp"] -= damage1
            print(f"{first_defender['name']} took {damage1} damage!")
            
            # Check if defender fainted
            if first_defender["current_hp"] <= 0:
                first_defender["current_hp"] = 0
                print(f"{first_defender['name']} fainted!")
                return (damage1, 0) if player_first else (0, damage1)
        
        # Second attack (if first defender didn't faint)
        print(f"{second_attacker['name']} used {second_move}!")
        damage2 = self.calculate_damage(second_attacker, second_defender, second_move)
        
        if damage2 > 0:
            second_defender["current_hp"] -= damage2
            print(f"{second_defender['name']} took {damage2} damage!")
            
            if second_defender["current_hp"] <= 0:
                second_defender["current_hp"] = 0
                print(f"{second_defender['name']} fainted!")
        
        # Process status effects
        status_damage1 = self.process_status_damage(first_attacker)
        first_attacker["current_hp"] -= status_damage1
        
        status_damage2 = self.process_status_damage(second_attacker)
        second_attacker["current_hp"] -= status_damage2
        
        if player_first:
            return (damage1, damage2)
        else:
            return (damage2, damage1)


def main():
    """Test battle engine"""
    print("=== Battle Engine Test ===\n")
    
    # Create test Pokémon
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
    
    squirtle = {
        "name": "Squirtle",
        "level": 25,
        "type1": "Water",
        "type2": None,
        "stats": {
            "hp": 90,
            "attack": 48,
            "defense": 65,
            "special_attack": 50,
            "special_defense": 64,
            "speed": 43
        },
        "current_hp": 90,
        "status": None
    }
    
    engine = BattleEngine()
    
    # Simulate battle turn
    print(f"{pikachu['name']} (HP: {pikachu['current_hp']}/{pikachu['stats']['hp']})")
    print(f"vs")
    print(f"{squirtle['name']} (HP: {squirtle['current_hp']}/{squirtle['stats']['hp']})\n")
    
    player_dmg, opponent_dmg = engine.execute_turn(
        pikachu, "Thunder Shock",
        squirtle, "Water Gun"
    )
    
    print(f"\n--- Turn Complete ---")
    print(f"{pikachu['name']}: {pikachu['current_hp']}/{pikachu['stats']['hp']} HP")
    print(f"{squirtle['name']}: {squirtle['current_hp']}/{squirtle['stats']['hp']} HP")


if __name__ == "__main__":
    main()
