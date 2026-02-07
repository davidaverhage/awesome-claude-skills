#!/usr/bin/env python3
"""
Battle AI for Gen VI Pokémon Game
Implements opponent AI decision-making for trainer battles.
"""

import random
import json
import os


class BattleAI:
    """AI opponent logic for selecting moves and switches"""
    
    DIFFICULTY_LEVELS = {
        "easy": {"smart_chance": 0.3, "switch_chance": 0.1},
        "normal": {"smart_chance": 0.6, "switch_chance": 0.3},
        "hard": {"smart_chance": 0.9, "switch_chance": 0.5}
    }
    
    def __init__(self, difficulty="normal"):
        """Initialize AI with difficulty setting"""
        self.difficulty = difficulty
        self.settings = self.DIFFICULTY_LEVELS.get(difficulty, self.DIFFICULTY_LEVELS["normal"])
        self.move_data = {}
        self.type_chart = self._load_type_chart()
        self._load_move_data()
    
    def _load_move_data(self):
        """Load move data for AI decision making"""
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
            print("Warning: move_data.json not found for AI")
    
    def _load_type_chart(self):
        """Load simplified type effectiveness chart"""
        return {
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
    
    def select_move(self, ai_pokemon, opponent_pokemon, available_moves):
        """
        Select the best move for AI Pokémon to use
        
        Args:
            ai_pokemon: Dict containing AI's Pokémon data
            opponent_pokemon: Dict containing player's Pokémon data
            available_moves: List of move names the AI can use
        
        Returns:
            str: Name of the selected move
        """
        if not available_moves:
            return "Tackle"  # Default move
        
        # Roll for smart decision
        if random.random() < self.settings["smart_chance"]:
            return self._select_smart_move(ai_pokemon, opponent_pokemon, available_moves)
        else:
            return random.choice(available_moves)
    
    def _select_smart_move(self, ai_pokemon, opponent_pokemon, available_moves):
        """Select move based on type effectiveness and strategy"""
        move_scores = {}
        
        for move_name in available_moves:
            if move_name not in self.move_data:
                move_scores[move_name] = 50  # Default score for unknown moves
                continue
            
            move = self.move_data[move_name]
            score = 50  # Base score
            
            # Factor 1: Move power
            if move["power"] > 0:
                score += move["power"] * 0.5
            
            # Factor 2: Type effectiveness
            effectiveness = self._calculate_effectiveness(
                move["type"],
                opponent_pokemon.get("type1"),
                opponent_pokemon.get("type2")
            )
            
            if effectiveness > 1.0:
                score += 30 * effectiveness
                print(f"AI considers {move_name}: Super effective! (effectiveness: {effectiveness}x)")
            elif effectiveness < 1.0:
                score -= 20
                if effectiveness == 0:
                    score = 0  # Never use ineffective moves
            
            # Factor 3: STAB bonus
            ai_type1 = ai_pokemon.get("type1")
            ai_type2 = ai_pokemon.get("type2")
            if move["type"] == ai_type1 or move["type"] == ai_type2:
                score += 15
            
            # Factor 4: Accuracy
            if move["accuracy"] < 100:
                score -= (100 - move["accuracy"]) * 0.3
            
            # Factor 5: PP consideration (avoid moves with very low PP unless necessary)
            if move["pp"] <= 5:
                score += 10  # Slightly favor powerful moves
            
            # Factor 6: Status moves evaluation
            if move["category"] == "Status":
                # Healing moves when low HP
                if "heal" in move.get("effect", "").lower():
                    hp_percent = ai_pokemon.get("current_hp", 100) / ai_pokemon["stats"]["hp"]
                    if hp_percent < 0.5:
                        score += 40
                    else:
                        score -= 20
                
                # Status-inducing moves
                elif opponent_pokemon.get("status") is None:
                    score += 25
                else:
                    score = 10  # Don't use status moves if opponent already has status
            
            # Factor 7: Priority moves when opponent is low HP
            if move.get("priority", 0) > 0:
                opponent_hp_percent = opponent_pokemon.get("current_hp", 100) / opponent_pokemon["stats"]["hp"]
                if opponent_hp_percent < 0.3:
                    score += 25  # Use priority moves to finish off weak opponents
            
            move_scores[move_name] = max(0, score)
        
        # Select move with highest score
        if not move_scores:
            return random.choice(available_moves)
        
        best_move = max(move_scores.items(), key=lambda x: x[1])
        print(f"AI selected: {best_move[0]} (score: {best_move[1]:.1f})")
        return best_move[0]
    
    def _calculate_effectiveness(self, move_type, defender_type1, defender_type2):
        """Calculate type effectiveness multiplier"""
        effectiveness = 1.0
        
        if move_type in self.type_chart:
            effectiveness *= self.type_chart[move_type].get(defender_type1, 1.0)
            if defender_type2:
                effectiveness *= self.type_chart[move_type].get(defender_type2, 1.0)
        
        return effectiveness
    
    def should_switch(self, ai_pokemon, opponent_pokemon, party):
        """
        Decide whether AI should switch Pokémon
        
        Args:
            ai_pokemon: Current AI Pokémon
            opponent_pokemon: Opponent's Pokémon
            party: List of AI's available Pokémon
        
        Returns:
            int or None: Index of Pokémon to switch to, or None to stay
        """
        # Don't switch if only one Pokémon or if random roll fails
        if len(party) <= 1 or random.random() > self.settings["switch_chance"]:
            return None
        
        # Check if current Pokémon is at a type disadvantage
        current_effectiveness = self._calculate_matchup_score(ai_pokemon, opponent_pokemon)
        
        # If current matchup is good, don't switch
        if current_effectiveness > 0:
            return None
        
        # Find better matchup in party
        best_switch_idx = None
        best_score = current_effectiveness
        
        for i, pokemon in enumerate(party):
            if pokemon == ai_pokemon or pokemon.get("current_hp", 0) <= 0:
                continue
            
            score = self._calculate_matchup_score(pokemon, opponent_pokemon)
            if score > best_score:
                best_score = score
                best_switch_idx = i
        
        if best_switch_idx is not None:
            print(f"AI considering switch to {party[best_switch_idx]['name']} (score: {best_score})")
        
        return best_switch_idx
    
    def _calculate_matchup_score(self, attacker, defender):
        """Calculate how favorable a matchup is"""
        score = 0
        
        # Check offensive advantage
        attacker_type1 = attacker.get("type1")
        attacker_type2 = attacker.get("type2")
        
        offensive_mult = max(
            self._calculate_effectiveness(attacker_type1, defender.get("type1"), defender.get("type2")),
            self._calculate_effectiveness(attacker_type2, defender.get("type1"), defender.get("type2")) if attacker_type2 else 0
        )
        
        score += (offensive_mult - 1.0) * 100
        
        # Check defensive advantage
        defender_type1 = defender.get("type1")
        defender_type2 = defender.get("type2")
        
        defensive_mult = max(
            self._calculate_effectiveness(defender_type1, attacker.get("type1"), attacker.get("type2")),
            self._calculate_effectiveness(defender_type2, attacker.get("type1"), attacker.get("type2")) if defender_type2 else 0
        )
        
        score -= (defensive_mult - 1.0) * 100
        
        return score


def main():
    """Test battle AI"""
    print("=== Battle AI Test ===\n")
    
    # Create test Pokémon
    charmander = {
        "name": "Charmander",
        "type1": "Fire",
        "type2": None,
        "stats": {"hp": 80, "attack": 52, "defense": 43, "special_attack": 60, "special_defense": 50, "speed": 65},
        "current_hp": 80
    }
    
    squirtle = {
        "name": "Squirtle",
        "type1": "Water",
        "type2": None,
        "stats": {"hp": 90, "attack": 48, "defense": 65, "special_attack": 50, "special_defense": 64, "speed": 43},
        "current_hp": 90
    }
    
    ai = BattleAI(difficulty="hard")
    
    # Test move selection
    available_moves = ["Ember", "Scratch", "Growl", "Smokescreen"]
    selected_move = ai.select_move(charmander, squirtle, available_moves)
    print(f"\nAI chose: {selected_move}")
    
    # Test with different matchup
    bulbasaur = {
        "name": "Bulbasaur",
        "type1": "Grass",
        "type2": "Poison",
        "stats": {"hp": 85, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45},
        "current_hp": 85
    }
    
    available_moves2 = ["Vine Whip", "Tackle", "Growl", "Leech Seed"]
    selected_move2 = ai.select_move(bulbasaur, squirtle, available_moves2)
    print(f"\nAI chose: {selected_move2}")


if __name__ == "__main__":
    main()
