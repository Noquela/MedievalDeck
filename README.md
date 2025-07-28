# Medieval Deck

Um jogo de cartas roguelike (deckbuilder) desenvolvido em Python com Pygame, inspirado em jogos como Slay the Spire.

## 🎮 Sobre o Jogo

Medieval Deck é um jogo de cartas onde você escolhe um herói medieval (Knight, Mage, Assassin) e enfrenta inimigos em combates por turnos. O jogo inclui:

- **3 Heróis únicos** com habilidades especiais
- **Sistema de cartas** com diferentes tipos (ataque, defesa, magia)
- **Progressão procedural** com eventos e lojas
- **Relíquias** que modificam o gameplay
- **Assets gerados por IA** para fundos e personagens

## 🚀 Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. (Opcional) Gere os assets com IA:
```bash
python generate_assets.py
```

3. Execute o jogo:
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
MedievalDeck/
├── main.py                    # Arquivo principal
├── config.py                  # Configurações globais
├── screens/                   # Telas do jogo
├── cards/                     # Sistema de cartas
├── utils/                     # Utilitários
├── gen_assets/               # Geração de assets com IA
├── assets/                   # Recursos visuais
└── audio/                    # Sons e música
```

## 🎯 Roadmap

O desenvolvimento está dividido em 15 sprints, desde a estrutura base até o MVP completo. Cada sprint implementa funcionalidades específicas conforme detalhado nos arquivos de roadmap.

## 🛠️ Tecnologias

- **Python 3.8+**
- **Pygame 2.5.2**
- **Pillow 10.0.1**
- **PyTorch 2.1.0** (otimizado para RTX 5070)
- **Stable Diffusion XL** (para geração de assets)
- **Diffusers 0.24.0** (pipeline de IA)

## 🎨 Geração de Assets

O jogo inclui um sistema de geração de assets com IA:

- **Backgrounds dinâmicos** para cada herói
- **Otimizado para RTX 5070** com SM120
- **Seed fixa** para reprodutibilidade
- **Prompts específicos** para cada personagem

## 📝 Licença

Este projeto está em desenvolvimento ativo. 