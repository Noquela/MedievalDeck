"""
Hero selection screen for Medieval Deck
Sprint 4 Implementation: RTX 5070 optimized AI generation with hero sprites
Dynamic backgrounds + character sprites with enhanced quality
"""

import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GOLD, HEROES
from utils.buttons import Button
from gen_assets.generate_backgrounds import AssetGenerator

class SelectionScreen:
    """
    Hero selection screen with AI-generated backgrounds
    Optimized for 3440x1440 ultrawide resolution
    """
    
    def __init__(self, game_instance):
        """
        Initialize selection screen
        
        Args:
            game_instance: Reference to main game instance
        """
        self.game = game_instance
        # Use mock for development, real SDXL in production
        import sys
        use_mock = 'test' in sys.argv[0] or '--test' in sys.argv
        self.asset_generator = AssetGenerator(use_mock=use_mock)
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 120)
        self.hero_font = pygame.font.Font(None, 80)
        self.desc_font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 60)
        
        # Selection state
        self.selected_hero = None
        self.current_hero_index = 0  # For arrow navigation
        self.heroes_list = ['knight', 'mage', 'assassin']
        self.hero_backgrounds = {}
        self.hero_sprites = {}
        self.ui_elements = {}
        self.current_background = None
        
        # Hero layout for ultrawide
        self.hero_positions = self._calculate_hero_positions()
        self.hero_buttons = {}
        self._setup_hero_buttons()
        
        # Confirm button
        self.confirm_button = Button(
            SCREEN_WIDTH - 350, SCREEN_HEIGHT - 120,
            300, 80, "CONFIRMAR", self.button_font,
            color=GOLD
        )
        
        # Back button
        self.back_button = Button(
            50, SCREEN_HEIGHT - 120,
            200, 80, "VOLTAR", self.button_font
        )
        
        # Navigation arrows
        self.left_arrow = Button(
            100, SCREEN_HEIGHT // 2 - 40,
            80, 80, "◀", self.hero_font
        )
        
        self.right_arrow = Button(
            SCREEN_WIDTH - 180, SCREEN_HEIGHT // 2 - 40,
            80, 80, "▶", self.hero_font
        )
        
        print("Selection screen initialized for Sprint 4")
        print("RTX 5070 optimized AI generation system ready")
        
        # Pre-generate backgrounds and sprites asynchronously
        self._preload_assets()
        
    def _calculate_hero_positions(self):
        """Calculate hero positions for ultrawide layout"""
        hero_width = 400
        hero_height = 600
        total_width = 3 * hero_width + 2 * 100  # 100px spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = SCREEN_HEIGHT // 2 - hero_height // 2
        
        positions = {}
        heroes = ['knight', 'mage', 'assassin']
        
        for i, hero in enumerate(heroes):
            x = start_x + i * (hero_width + 100)
            positions[hero] = {
                'rect': pygame.Rect(x, y, hero_width, hero_height),
                'name_pos': (x + hero_width // 2, y - 50),
                'desc_pos': (x + hero_width // 2, y + hero_height + 20)
            }
            
        return positions
        
    def _setup_hero_buttons(self):
        """Setup clickable areas for heroes"""
        for hero, pos_data in self.hero_positions.items():
            rect = pos_data['rect']
            self.hero_buttons[hero] = Button(
                rect.x, rect.y, rect.width, rect.height,
                "", self.hero_font, 
                bg_color=(0, 0, 0, 0)  # Transparent
            )
            
    def _preload_assets(self):
        """Preload hero backgrounds and sprites with RTX 5070 optimization"""
        print("Preloading hero assets with RTX 5070 optimization...")
        
        try:
            # Generate all backgrounds
            self.hero_backgrounds = self.asset_generator.generate_all_hero_backgrounds()
            print(f"Loaded {len(self.hero_backgrounds)} RTX optimized backgrounds")
            
            # Generate all hero sprites
            self.hero_sprites = self.asset_generator.generate_all_hero_sprites()
            print(f"Loaded {len(self.hero_sprites)} high-quality hero sprites")
            
            # Generate UI elements (arrows, etc.)
            self.ui_elements = self.asset_generator.generate_all_ui_elements()
            print(f"Loaded {len(self.ui_elements)} UI elements")
            
            # Set default hero and background
            self.selected_hero = self.heroes_list[0]
            self._load_background(self.selected_hero)
                
        except Exception as e:
            print(f"Warning: Asset preloading failed: {e}")
            print("Using fallback rendering")
            
    def _load_background(self, hero_type):
        """
        Load and scale background for hero
        
        Args:
            hero_type: Hero to load background for
        """
        if hero_type in self.hero_backgrounds:
            bg_path = self.hero_backgrounds[hero_type]
            
            try:
                # Load and scale background
                background = pygame.image.load(bg_path)
                self.current_background = pygame.transform.scale(
                    background, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
                print(f"Background loaded for {hero_type}")
                
            except Exception as e:
                print(f"Error loading background for {hero_type}: {e}")
                self.current_background = None
        else:
            self.current_background = None
            
    def handle_events(self, events):
        """
        Handle selection screen events
        
        Args:
            events: List of pygame events
            
        Returns:
            str: Next game state or None
        """
        for event in events:
            # Check arrow navigation
            if self.left_arrow.handle_event(event):
                self._navigate_hero(-1)
                
            if self.right_arrow.handle_event(event):
                self._navigate_hero(1)
            
            # Check hero selection (for direct clicking)
            for hero, button in self.hero_buttons.items():
                if button.handle_event(event):
                    self._select_hero(hero)
                    
            # Check confirm button
            if self.confirm_button.handle_event(event):
                if self.selected_hero:
                    self.game.selected_hero = self.selected_hero
                    print(f"Hero selected: {self.selected_hero}")
                    return "gameplay"  # Transition to combat
                    
            # Check back button
            if self.back_button.handle_event(event):
                return "menu"  # Return to menu
                
            # Keyboard navigation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self._navigate_hero(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self._navigate_hero(1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_hero:
                        self.game.selected_hero = self.selected_hero
                        return "gameplay"
                
        return None
        
    def _navigate_hero(self, direction):
        """
        Navigate between heroes using arrows
        
        Args:
            direction: -1 for left, 1 for right
        """
        self.current_hero_index = (self.current_hero_index + direction) % len(self.heroes_list)
        new_hero = self.heroes_list[self.current_hero_index]
        self._select_hero(new_hero)
        
    def _select_hero(self, hero_type):
        """
        Select a hero and update display
        
        Args:
            hero_type: Selected hero type
        """
        if hero_type != self.selected_hero:
            # Update index for consistency
            if hero_type in self.heroes_list:
                self.current_hero_index = self.heroes_list.index(hero_type)
            
            self.selected_hero = hero_type
            self._load_background(hero_type)
            print(f"Selected hero: {hero_type}")
            
    def update(self):
        """Update selection screen logic"""
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.hero_buttons.values():
            # Simulate mouse motion for hover detection
            fake_event = type('FakeEvent', (), {
                'type': pygame.MOUSEMOTION,
                'pos': mouse_pos
            })()
            button.handle_event(fake_event)
            
    def render(self, screen):
        """
        Render hero selection screen
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BLACK)
        
        # Draw background if available
        if self.current_background:
            screen.blit(self.current_background, (0, 0))
        else:
            # Fallback gradient background
            self._draw_fallback_background(screen)
            
        # Draw title
        title = self.title_font.render("ESCOLHA SEU HERÓI", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw current hero (single hero display)
        self._draw_current_hero(screen)
        
        # Draw navigation arrows
        self._draw_navigation_arrows(screen)
        
        # Draw hero description
        if self.selected_hero:
            self._draw_hero_description(screen)
            
        # Draw buttons
        self.confirm_button.draw(screen)
        self.back_button.draw(screen)
        self.left_arrow.draw(screen)
        self.right_arrow.draw(screen)
        
        # Draw sprint indicator
        sprint_text = self.desc_font.render("Sprint 4: RTX 5070 Optimized AI + Hero Sprites", True, WHITE)
        sprint_rect = sprint_text.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
        screen.blit(sprint_text, sprint_rect)
        
    def _draw_fallback_background(self, screen):
        """Draw fallback background when AI assets aren't available"""
        # Create gothic gradient
        for y in range(SCREEN_HEIGHT):
            intensity = int(64 * (1 - y / SCREEN_HEIGHT))
            color = (intensity // 2, intensity // 4, intensity)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
    
    def _draw_current_hero(self, screen):
        """Draw the currently selected hero in center screen"""
        if not self.selected_hero:
            return
            
        # Center position for hero display
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Hero container
        hero_rect = pygame.Rect(center_x - 300, center_y - 200, 600, 400)
        pygame.draw.rect(screen, (16, 16, 24), hero_rect)
        pygame.draw.rect(screen, GOLD, hero_rect, 6)
        
        # Draw AI-generated sprite if available
        if self.selected_hero in self.hero_sprites and os.path.exists(self.hero_sprites[self.selected_hero]):
            try:
                sprite_image = pygame.image.load(self.hero_sprites[self.selected_hero])
                
                # Scale sprite for center display
                sprite_size = 300
                sprite_image = pygame.transform.scale(sprite_image, (sprite_size, sprite_size))
                
                # Center sprite
                sprite_rect = sprite_image.get_rect(center=(center_x, center_y - 30))
                screen.blit(sprite_image, sprite_rect)
                
                # Glow effect
                glow_surface = pygame.Surface((sprite_size + 40, sprite_size + 40))
                glow_surface.set_alpha(40)
                glow_surface.fill(GOLD)
                glow_rect = glow_surface.get_rect(center=sprite_rect.center)
                screen.blit(glow_surface, glow_rect)
                
            except Exception as e:
                print(f"Error loading sprite for {self.selected_hero}: {e}")
                self._draw_hero_placeholder_center(screen, center_x, center_y)
        else:
            self._draw_hero_placeholder_center(screen, center_x, center_y)
        
        # Draw hero name below
        hero_data = HEROES[self.selected_hero]
        name_surface = self.title_font.render(hero_data['name'], True, GOLD)
        name_rect = name_surface.get_rect(center=(center_x, center_y + 180))
        screen.blit(name_surface, name_rect)
        
        # Draw stats
        stats = [f"Health: {hero_data['health']}", f"Mana: {hero_data['mana']}"]
        stats_text = " | ".join(stats)
        stats_surface = self.hero_font.render(stats_text, True, WHITE)
        stats_rect = stats_surface.get_rect(center=(center_x, center_y + 220))
        screen.blit(stats_surface, stats_rect)
    
    def _draw_hero_placeholder_center(self, screen, center_x, center_y):
        """Draw placeholder for center hero display"""
        placeholder_rect = pygame.Rect(center_x - 150, center_y - 150, 300, 300)
        pygame.draw.rect(screen, (64, 64, 64), placeholder_rect)
        pygame.draw.rect(screen, WHITE, placeholder_rect, 4)
        
        # Draw hero initial
        initial = self.selected_hero[0].upper()
        initial_font = pygame.font.Font(None, 200)
        initial_surface = initial_font.render(initial, True, WHITE)
        initial_rect = initial_surface.get_rect(center=placeholder_rect.center)
        screen.blit(initial_surface, initial_rect)
    
    def _draw_navigation_arrows(self, screen):
        """Draw navigation arrows with AI-generated graphics if available"""
        # Left arrow
        if 'arrow_left' in self.ui_elements and os.path.exists(self.ui_elements['arrow_left']):
            try:
                arrow_img = pygame.image.load(self.ui_elements['arrow_left'])
                arrow_img = pygame.transform.scale(arrow_img, (60, 60))
                arrow_rect = arrow_img.get_rect(center=self.left_arrow.rect.center)
                screen.blit(arrow_img, arrow_rect)
            except:
                pass  # Fallback to button text
        
        # Right arrow  
        if 'arrow_right' in self.ui_elements and os.path.exists(self.ui_elements['arrow_right']):
            try:
                arrow_img = pygame.image.load(self.ui_elements['arrow_right'])
                arrow_img = pygame.transform.scale(arrow_img, (60, 60))
                arrow_rect = arrow_img.get_rect(center=self.right_arrow.rect.center)
                screen.blit(arrow_img, arrow_rect)
            except:
                pass  # Fallback to button text
        
        # Hero counter
        counter_text = f"{self.current_hero_index + 1} / {len(self.heroes_list)}"
        counter_surface = self.desc_font.render(counter_text, True, WHITE)
        counter_rect = counter_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 180))
        screen.blit(counter_surface, counter_rect)
            
    def _draw_heroes_with_sprites(self, screen):
        """Draw hero selection areas with AI-generated sprites"""
        for hero, pos_data in self.hero_positions.items():
            rect = pos_data['rect']
            
            # Draw hero container
            border_color = GOLD if hero == self.selected_hero else WHITE
            pygame.draw.rect(screen, (16, 16, 24), rect)  # Darker background
            pygame.draw.rect(screen, border_color, rect, 4)
            
            # Draw AI-generated sprite if available
            if hero in self.hero_sprites and os.path.exists(self.hero_sprites[hero]):
                try:
                    sprite_image = pygame.image.load(self.hero_sprites[hero])
                    
                    # Scale sprite to fit in hero area (maintaining aspect ratio)
                    sprite_size = min(rect.width - 40, rect.height - 120)
                    sprite_image = pygame.transform.scale(sprite_image, (sprite_size, sprite_size))
                    
                    # Center sprite in hero area
                    sprite_rect = sprite_image.get_rect(center=(rect.centerx, rect.centery - 20))
                    screen.blit(sprite_image, sprite_rect)
                    
                    # Add subtle glow effect for selected hero
                    if hero == self.selected_hero:
                        glow_surface = pygame.Surface((sprite_size + 20, sprite_size + 20))
                        glow_surface.set_alpha(30)
                        glow_surface.fill(GOLD)
                        glow_rect = glow_surface.get_rect(center=sprite_rect.center)
                        screen.blit(glow_surface, glow_rect)
                        
                except Exception as e:
                    print(f"Error loading sprite for {hero}: {e}")
                    self._draw_hero_placeholder(screen, hero, rect)
            else:
                self._draw_hero_placeholder(screen, hero, rect)
            
            # Draw hero name below sprite
            hero_data = HEROES[hero]
            name_surface = self.hero_font.render(hero_data['name'], True, border_color)
            name_rect = name_surface.get_rect(center=(rect.centerx, rect.bottom - 60))
            screen.blit(name_surface, name_rect)
            
            # Draw stats below name
            stats = [f"HP: {hero_data['health']}", f"MP: {hero_data['mana']}"]
            stats_text = " | ".join(stats)
            stats_surface = self.desc_font.render(stats_text, True, WHITE)
            stats_rect = stats_surface.get_rect(center=(rect.centerx, rect.bottom - 25))
            screen.blit(stats_surface, stats_rect)
    
    def _draw_hero_placeholder(self, screen, hero, rect):
        """Draw placeholder when sprite is not available"""
        # Draw simple placeholder
        placeholder_color = (64, 64, 64)
        placeholder_rect = pygame.Rect(
            rect.centerx - 100, rect.centery - 100, 200, 200
        )
        pygame.draw.rect(screen, placeholder_color, placeholder_rect)
        pygame.draw.rect(screen, WHITE, placeholder_rect, 2)
        
        # Draw hero initial
        initial = hero[0].upper()
        initial_font = pygame.font.Font(None, 120)
        initial_surface = initial_font.render(initial, True, WHITE)
        initial_rect = initial_surface.get_rect(center=placeholder_rect.center)
        screen.blit(initial_surface, initial_rect)
                
    def _draw_selection_indicator(self, screen):
        """Draw indicator around selected hero"""
        if self.selected_hero in self.hero_positions:
            rect = self.hero_positions[self.selected_hero]['rect']
            # Animated selection border
            border_width = 6
            pygame.draw.rect(screen, GOLD, rect.inflate(border_width * 2, border_width * 2), border_width)
            
    def _draw_hero_description(self, screen):
        """Draw detailed description of selected hero"""
        if self.selected_hero:
            hero_data = HEROES[self.selected_hero]
            
            # Description box
            desc_rect = pygame.Rect(50, SCREEN_HEIGHT - 300, SCREEN_WIDTH - 100, 150)
            pygame.draw.rect(screen, (0, 0, 0, 180), desc_rect)
            pygame.draw.rect(screen, GOLD, desc_rect, 3)
            
            # Description text
            desc_surface = self.desc_font.render(hero_data['description'], True, WHITE)
            desc_text_rect = desc_surface.get_rect(center=desc_rect.center)
            screen.blit(desc_surface, desc_text_rect)