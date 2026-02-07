#!/usr/bin/env python3
"""
Main Game Loop for Gen VI Pokémon Game
Handles initialization, state management, and the main update/render loop.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pygame
except ImportError:
    print("Warning: pygame not installed. Running in headless mode.")
    pygame = None


class GameState:
    """Game state enumeration"""
    TITLE_SCREEN = "title_screen"
    OVERWORLD = "overworld"
    BATTLE = "battle"
    MENU = "menu"
    DIALOGUE = "dialogue"


class PokemonGame:
    """Main game class managing the entire game loop"""
    
    def __init__(self):
        """Initialize game systems"""
        self.running = True
        self.state = GameState.TITLE_SCREEN
        self.clock = None
        self.screen = None
        self.fps = 60
        
        # Game systems
        self.player = None
        self.current_map = None
        self.battle_system = None
        self.save_system = None
        
        # Initialize pygame if available
        if pygame:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Gen VI Pokémon Game")
            self.clock = pygame.time.Clock()
        
        # Load game data
        self._load_game_data()
        
        print("=== Gen VI Pokémon Game Initialized ===")
        print("Game State: TITLE_SCREEN")
        print("Press SPACE to start (or CTRL+C to quit)")
    
    def _load_game_data(self):
        """Load core game data from JSON files"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load Pokémon data
        try:
            with open(os.path.join(base_path, "pokemon", "base_stats.json"), 'r') as f:
                data = json.load(f)
                self.pokemon_data = data.get("pokemon", [])
            print(f"Loaded {len(self.pokemon_data)} Pokémon species")
        except FileNotFoundError:
            print("Warning: pokemon/base_stats.json not found")
            self.pokemon_data = []
        
        # Load move data
        try:
            with open(os.path.join(base_path, "moves", "move_data.json"), 'r') as f:
                data = json.load(f)
                self.move_data = data.get("moves", [])
            print(f"Loaded {len(self.move_data)} moves")
        except FileNotFoundError:
            print("Warning: moves/move_data.json not found")
            self.move_data = []
        
        # Load map data
        try:
            with open(os.path.join(base_path, "overworld", "maps", "map_headers.json"), 'r') as f:
                data = json.load(f)
                self.map_data = data.get("maps", [])
            print(f"Loaded {len(self.map_data)} maps")
        except FileNotFoundError:
            print("Warning: overworld/maps/map_headers.json not found")
            self.map_data = []
    
    def handle_input(self):
        """Process player input"""
        if pygame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_keypress(event.key)
        else:
            # Headless mode - simple input
            try:
                import select
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.readline().strip()
                    if key.lower() == 'q':
                        self.running = False
                    elif key == ' ':
                        self._handle_keypress(pygame.K_SPACE if pygame else ord(' '))
            except:
                pass
    
    def _handle_keypress(self, key):
        """Handle individual key press"""
        if pygame and key == pygame.K_SPACE:
            if self.state == GameState.TITLE_SCREEN:
                self.state = GameState.OVERWORLD
                print("\n=== Entering Overworld ===")
                print("Use Arrow Keys to move, ENTER for menu")
        elif pygame and key == pygame.K_RETURN:
            if self.state == GameState.OVERWORLD:
                self.state = GameState.MENU
                print("\n=== Menu Opened ===")
        elif pygame and key == pygame.K_ESCAPE:
            if self.state == GameState.MENU:
                self.state = GameState.OVERWORLD
                print("\n=== Returned to Overworld ===")
    
    def update(self, delta_time):
        """Update game logic"""
        if self.state == GameState.OVERWORLD:
            self._update_overworld(delta_time)
        elif self.state == GameState.BATTLE:
            self._update_battle(delta_time)
        elif self.state == GameState.MENU:
            self._update_menu(delta_time)
    
    def _update_overworld(self, delta_time):
        """Update overworld state"""
        # Handle player movement, NPC updates, etc.
        pass
    
    def _update_battle(self, delta_time):
        """Update battle state"""
        # Handle battle logic
        pass
    
    def _update_menu(self, delta_time):
        """Update menu state"""
        # Handle menu navigation
        pass
    
    def render(self):
        """Render current game state"""
        if not pygame:
            return
        
        self.screen.fill((0, 0, 0))  # Black background
        
        if self.state == GameState.TITLE_SCREEN:
            self._render_title_screen()
        elif self.state == GameState.OVERWORLD:
            self._render_overworld()
        elif self.state == GameState.BATTLE:
            self._render_battle()
        elif self.state == GameState.MENU:
            self._render_menu()
        
        pygame.display.flip()
    
    def _render_title_screen(self):
        """Render title screen"""
        font = pygame.font.Font(None, 72)
        title = font.render("Pokémon Gen VI", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 200))
        self.screen.blit(title, title_rect)
        
        font_small = pygame.font.Font(None, 36)
        prompt = font_small.render("Press SPACE to Start", True, (200, 200, 200))
        prompt_rect = prompt.get_rect(center=(400, 400))
        self.screen.blit(prompt, prompt_rect)
    
    def _render_overworld(self):
        """Render overworld"""
        # Placeholder: Draw grid for map
        grid_size = 32
        for x in range(0, 800, grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, 600))
        for y in range(0, 600, grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (800, y))
        
        # Draw player placeholder
        pygame.draw.circle(self.screen, (255, 100, 100), (400, 300), 16)
        
        font = pygame.font.Font(None, 24)
        text = font.render("Overworld - Press ENTER for Menu", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
    
    def _render_battle(self):
        """Render battle screen"""
        font = pygame.font.Font(None, 48)
        text = font.render("BATTLE!", True, (255, 255, 255))
        self.screen.blit(text, (300, 250))
    
    def _render_menu(self):
        """Render menu"""
        pygame.draw.rect(self.screen, (50, 50, 50), (200, 150, 400, 300))
        pygame.draw.rect(self.screen, (255, 255, 255), (200, 150, 400, 300), 2)
        
        font = pygame.font.Font(None, 36)
        menu_items = ["Pokédex", "Pokémon", "Bag", "Save", "Options", "Exit"]
        for i, item in enumerate(menu_items):
            text = font.render(item, True, (255, 255, 255))
            self.screen.blit(text, (250, 180 + i * 40))
        
        font_small = pygame.font.Font(None, 24)
        prompt = font_small.render("Press ESC to close", True, (200, 200, 200))
        self.screen.blit(prompt, (250, 500))
    
    def run(self):
        """Main game loop"""
        last_time = 0
        
        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks() if pygame else 0
            delta_time = (current_time - last_time) / 1000.0 if last_time > 0 else 0.016
            last_time = current_time
            
            # Process input
            self.handle_input()
            
            # Update game state
            self.update(delta_time)
            
            # Render
            self.render()
            
            # Cap framerate
            if self.clock:
                self.clock.tick(self.fps)
        
        # Cleanup
        if pygame:
            pygame.quit()
        print("\n=== Game Shutdown ===")


def main():
    """Entry point"""
    game = PokemonGame()
    game.run()


if __name__ == "__main__":
    main()
