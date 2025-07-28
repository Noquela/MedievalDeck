"""
Script principal para geração de assets do Medieval Deck
Otimizado para RTX 5070
"""

import sys
import os

# Adiciona o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gen_assets.generate_backgrounds import AssetGenerator

def main():
    """Script principal para gerar assets"""
    print("=== Medieval Deck - Gerador de Assets ===")
    print("Otimizado para RTX 5070 com SM120")
    print()
    
    try:
        # Inicializa o gerador
        generator = AssetGenerator(seed=42)
        
        print("Escolha uma opção:")
        print("1. Gerar backgrounds para todos os heróis")
        print("2. Gerar background específico")
        print("3. Forçar regeneração de todos")
        print("4. Sair")
        
        while True:
            choice = input("\nDigite sua escolha (1-4): ").strip()
            
            if choice == "1":
                print("\nGerando backgrounds para todos os heróis...")
                generator.generate_all_backgrounds()
                break
                
            elif choice == "2":
                print("\nHeróis disponíveis: knight, mage, assassin")
                hero = input("Digite o ID do herói: ").strip().lower()
                
                if hero in ['knight', 'mage', 'assassin']:
                    generator.generate_background(hero)
                else:
                    print("Herói inválido!")
                break
                
            elif choice == "3":
                print("\nForçando regeneração de todos os backgrounds...")
                generator.generate_all_backgrounds(force_regenerate=True)
                break
                
            elif choice == "4":
                print("Saindo...")
                break
                
            else:
                print("Opção inválida!")
        
        print("\nGeração concluída!")
        
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nErro durante a geração: {e}")
    finally:
        # Limpa recursos
        if 'generator' in locals():
            generator.cleanup()

if __name__ == "__main__":
    main() 