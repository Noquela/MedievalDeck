"""
Art Direction System for Medieval Deck
Implements consistent SDXL prompts based on art.txt guidelines
Gothic medieval realism with artistic touch
"""

from config import AI_SEED, AI_IMAGE_SIZE

class ArtDirection:
    """
    Centralized art direction system following established guidelines
    """
    
    # Base style constants
    BASE_STYLE = "Medieval gothic art, realistic digital painting, dramatic lighting, cinematic composition"
    NEGATIVE_PROMPT = "cartoon, anime, low quality, blurry, modern, contemporary, plastic, toy-like"
    
    # Color palettes
    COLD_PALETTE = "deep blue, grey, violet tones, golden highlights"
    WARM_PALETTE = "crimson red, emerald green, warm gold accents"
    
    # Quality settings
    QUALITY_TAGS = "highly detailed, masterpiece, best quality, sharp focus, professional artwork"
    
    @classmethod
    def get_hero_background_prompt(cls, hero_type):
        """
        Generate specific background prompts for each hero
        
        Args:
            hero_type: 'knight', 'mage', or 'assassin'
            
        Returns:
            dict: Complete prompt configuration
        """
        prompts = {
            'knight': {
                'positive': f"""
                Medieval knight throne room, gothic stone architecture, ornate religious carvings,
                epic torchlight casting dramatic shadows, heavy wooden doors with iron bindings,
                stained glass windows, ceremonial banners, noble atmosphere,
                {cls.BASE_STYLE}, {cls.COLD_PALETTE}, {cls.QUALITY_TAGS}
                """.strip(),
                'scene_desc': 'Noble throne room with gothic architecture'
            },
            
            'mage': {
                'positive': f"""
                Ancient wizard tower library, floating magical tomes, glowing arcane circles,
                mystical purple and blue lighting, stone walls covered in runes,
                bubbling alchemical apparatus, starlight through tall windows,
                ethereal magical atmosphere, crystalline formations,
                {cls.BASE_STYLE}, deep violet and sapphire tones, {cls.QUALITY_TAGS}
                """.strip(),
                'scene_desc': 'Mystical tower filled with magical knowledge'
            },
            
            'assassin': {
                'positive': f"""
                Dark medieval alleyway, moonlit stone passages, climbing ivy on walls,
                hidden doorways and secret passages, subtle fog and mist,
                weathered cobblestones, shadowy corners, mysterious atmosphere,
                abandoned medieval courtyard at night, stealth and secrecy,
                {cls.BASE_STYLE}, muted greys and blacks with silver moonlight, {cls.QUALITY_TAGS}
                """.strip(),
                'scene_desc': 'Shadowy medieval passages perfect for stealth'
            }
        }
        
        base_config = prompts.get(hero_type, prompts['knight'])
        base_config.update({
            'negative': cls.NEGATIVE_PROMPT,
            'width': AI_IMAGE_SIZE[0],
            'height': AI_IMAGE_SIZE[1],
            'seed': AI_SEED,
            'hero': hero_type
        })
        
        return base_config
    
    @classmethod
    def get_hero_sprite_prompt(cls, hero_type):
        """
        Generate hero character sprite prompts
        
        Args:
            hero_type: 'knight', 'mage', or 'assassin'
            
        Returns:
            dict: Complete sprite prompt configuration
        """
        sprites = {
            'knight': {
                'positive': f"""
                Medieval knight in full plate armor, ornate religious engravings on armor,
                polished steel with golden accents, ceremonial sword and shield,
                noble stance, determined expression, detailed metalwork,
                battle-worn but dignified, heroic proportions,
                {cls.BASE_STYLE}, {cls.QUALITY_TAGS}
                """.strip(),
                'character_desc': 'Noble armored warrior'
            },
            
            'mage': {
                'positive': f"""
                Medieval wizard in dark purple robes, glowing magical effects around hands,
                arcane staff with crystal top, wise aged face with glowing eyes,
                mystical aura, floating spell components, intricate robe patterns,
                scholarly yet powerful appearance, magical energy swirling,
                {cls.BASE_STYLE}, {cls.QUALITY_TAGS}
                """.strip(),
                'character_desc': 'Powerful spellcaster'
            },
            
            'assassin': {
                'positive': f"""
                Medieval rogue in dark leather armor, hooded cloak with hood up,
                twin curved daggers, agile athletic build, mysterious face in shadows,
                stealthy posture, dark colors with subtle metallic accents,
                nimble and dangerous appearance, ready for action,
                {cls.BASE_STYLE}, {cls.QUALITY_TAGS}
                """.strip(),
                'character_desc': 'Swift shadow warrior'
            }
        }
        
        base_config = sprites.get(hero_type, sprites['knight'])
        base_config.update({
            'negative': cls.NEGATIVE_PROMPT,
            'width': 1024,
            'height': 1024,
            'seed': AI_SEED + hash(hero_type) % 1000,  # Slight seed variation
            'hero': hero_type
        })
        
        return base_config
    
    @classmethod
    def get_ui_element_prompt(cls, element_type):
        """
        Generate UI element prompts
        
        Args:
            element_type: Type of UI element
            
        Returns:
            dict: Complete UI prompt configuration
        """
        ui_elements = {
            'button': {
                'positive': f"""
                Medieval parchment button, aged paper texture, ornate border,
                manuscript style, weathered edges, subtle embossing,
                {cls.BASE_STYLE}, {cls.QUALITY_TAGS}
                """.strip(),
                'desc': 'Medieval style UI button'
            },
            
            'frame': {
                'positive': f"""
                Ornate medieval frame, carved stone border, gothic details,
                weathered texture, architectural elements,
                {cls.BASE_STYLE}, {cls.QUALITY_TAGS}
                """.strip(),
                'desc': 'Gothic stone frame'
            }
        }
        
        base_config = ui_elements.get(element_type, ui_elements['button'])
        base_config.update({
            'negative': cls.NEGATIVE_PROMPT,
            'width': 512,
            'height': 512,
            'seed': AI_SEED,
            'element': element_type
        })
        
        return base_config