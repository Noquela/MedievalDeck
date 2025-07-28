"""
Sistema de geração de backgrounds com Stable Diffusion XL
Otimizado para RTX 5070 com SM120
"""

import os
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import numpy as np
from config import *

class AssetGenerator:
    def __init__(self, seed=42):
        """
        Inicializa o gerador de assets
        
        Args:
            seed: Seed fixa para reprodutibilidade
        """
        self.seed = seed
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Configurações otimizadas para RTX 5070
        self.model_id = "stabilityai/stable-diffusion-xl-base-1.0"
        self.pipeline = None
        
        # Prompts específicos para cada herói
        self.hero_prompts = {
            'knight': {
                'positive': "medieval castle hall, stone walls, torches, knight's armor on display, epic fantasy atmosphere, high quality, detailed",
                'negative': "modern, low quality, blurry, distorted"
            },
            'mage': {
                'positive': "ancient magical tower, floating books, crystal orbs, mystical energy, wizard's study, fantasy magic, high quality, detailed",
                'negative': "modern, low quality, blurry, distorted"
            },
            'assassin': {
                'positive': "dark shadowy alley, medieval city rooftops, stealth atmosphere, assassin's hideout, mysterious, high quality, detailed",
                'negative': "modern, low quality, blurry, distorted"
            }
        }
        
        # Garante que a pasta de backgrounds existe
        os.makedirs(BACKGROUNDS_PATH, exist_ok=True)
        
    def load_model(self):
        """Carrega o modelo SDXL otimizado para RTX 5070"""
        if self.pipeline is None:
            print("Carregando modelo Stable Diffusion XL...")
            
            # Configurações otimizadas para RTX 5070
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16,  # Usa FP16 para economizar VRAM
                use_safetensors=True,
                variant="fp16"
            )
            
            # Move para GPU e otimiza
            self.pipeline = self.pipeline.to(self.device)
            
            # Otimizações específicas para RTX 5070
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
                self.pipeline.enable_vae_slicing()
                self.pipeline.enable_model_cpu_offload()
            
            print("Modelo carregado com sucesso!")
    
    def generate_background(self, hero_id, force_regenerate=False):
        """
        Gera background para um herói específico
        
        Args:
            hero_id: ID do herói ('knight', 'mage', 'assassin')
            force_regenerate: Se True, regenera mesmo se já existir
            
        Returns:
            str: Caminho da imagem gerada
        """
        if hero_id not in self.hero_prompts:
            raise ValueError(f"Herói '{hero_id}' não encontrado")
        
        # Nome do arquivo
        filename = f"bg_{hero_id}_hall.png"
        filepath = os.path.join(BACKGROUNDS_PATH, filename)
        
        # Verifica se já existe e não precisa regenerar
        if os.path.exists(filepath) and not force_regenerate:
            print(f"Background para {hero_id} já existe: {filepath}")
            return filepath
        
        # Carrega modelo se necessário
        self.load_model()
        
        # Obtém prompts do herói
        prompts = self.hero_prompts[hero_id]
        
        print(f"Gerando background para {hero_id}...")
        
        # Gera a imagem
        with torch.no_grad():
            image = self.pipeline(
                prompt=prompts['positive'],
                negative_prompt=prompts['negative'],
                height=SCREEN_HEIGHT,
                width=SCREEN_WIDTH,
                num_inference_steps=30,  # Otimizado para qualidade/velocidade
                guidance_scale=7.5,
                generator=torch.Generator(device=self.device).manual_seed(self.seed)
            ).images[0]
        
        # Salva a imagem
        image.save(filepath)
        print(f"Background salvo: {filepath}")
        
        return filepath
    
    def generate_all_backgrounds(self, force_regenerate=False):
        """
        Gera backgrounds para todos os heróis
        
        Args:
            force_regenerate: Se True, regenera todas as imagens
        """
        print("Iniciando geração de backgrounds para todos os heróis...")
        
        for hero_id in self.hero_prompts.keys():
            try:
                self.generate_background(hero_id, force_regenerate)
            except Exception as e:
                print(f"Erro ao gerar background para {hero_id}: {e}")
        
        print("Geração de backgrounds concluída!")
    
    def cleanup(self):
        """Limpa recursos da GPU"""
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

def main():
    """Função principal para testar a geração"""
    generator = AssetGenerator()
    
    try:
        # Gera backgrounds para todos os heróis
        generator.generate_all_backgrounds()
        
        print("Todos os backgrounds foram gerados com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a geração: {e}")
    
    finally:
        generator.cleanup()

if __name__ == "__main__":
    main() 