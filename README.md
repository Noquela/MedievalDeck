# 🏰 Medieval Deck - Roguelike Card Game

**AI-Generated Assets • RTX 5070 Optimized • 3440x1440 Ultrawide**

## 🎮 Features

- **Real AI-Generated Assets**: Using Stable Diffusion XL with RTX 5070 optimization
- **3440x1440 Ultrawide Support**: Native ultrawide gaming experience
- **Medieval Theme**: Fantasy card game with knights, goblins, and medieval aesthetics
- **Performance Optimized**: 60+ FPS with XFormers memory optimization

## 🖼️ AI Asset Pipeline

All visual assets are generated using:
- **Stable Diffusion XL** (SDXL) for high-quality imagery
- **PyTorch 2.7.0 + CUDA 12.8** for RTX 5070 acceleration
- **XFormers 0.0.30** for memory-efficient attention
- **Custom prompts** optimized for medieval fantasy themes

## 🚀 Development Status

### ✅ Sprint 00 - Foundation (COMPLETE)
- Poetry dependency management
- 3440×1440 pygame window with FPS counter
- Main game loop with screen management
- GitHub Actions CI workflow
- Automated testing setup

### ✅ Sprint 01 - AI Assets (COMPLETE)
- ✅ SDXL pipeline with RTX 5070 optimization
- ✅ Arena background (3440x1440)
- ✅ Medieval card frame (512x768)
- ✅ Knight sprite sheets (5120x512, 10 frames)
- ✅ Goblin sprite sheets (4240x424, 10 frames)
- ✅ Additional backgrounds (menu, card_selection)
- ✅ Cache system for generated assets
- ✅ All core visual assets generated

### ✅ Sprint 02 - UI & Game Flow (COMPLETE)
- ✅ Screen management system with fade transitions
- ✅ MenuScreen with AI background
- ✅ CharacterSelectScreen with character options
- ✅ CombatScreen with arena and basic combat
- ✅ Navigation flow: Menu → Selection → Combat
- ✅ 8/8 tests passing for screen system
- ✅ Resource loading with caching

### 🔄 Sprint 03 - Card Game Mechanics (PLANNED)
- Card deck system and hand management
- Combat mechanics and turn-based gameplay
- Mage and Archer character implementations
- Save/load system
- Victory/defeat screens and progression
- Advanced combat animations

## Como Rodar

### Pré-requisitos

- Python 3.11+
- Poetry (gerenciador de dependências)

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repo>
cd medieval-deck
```

2. Instale as dependências:
```bash
poetry install
```

3. Ative o ambiente virtual:
```bash
poetry shell
```

4. Execute o jogo:
```bash
python src/main.py
```

### Gerar Assets (Arte IA)

Para gerar os assets visuais usando Stable Diffusion XL:

```bash
python scripts/gen_assets.py
```

### Executar Testes

```bash
pytest -q
```

## Estrutura do Projeto

```
medieval-deck/
├─ assets/               # Arquivos PNG gerados
│   ├─ bg/              # Backgrounds
│   ├─ sheets/          # Sprite sheets de personagens  
│   └─ ui/              # Interface do usuário
├─ scripts/
│   └─ gen_assets.py    # Pipeline de geração de arte IA
├─ src/
│   ├─ engine/          # Utilitários de engine
│   ├─ game/            # Lógica pura do jogo
│   ├─ ui/              # Telas do jogo
│   └─ main.py          # Loop principal
└─ tests/               # Testes automatizados
```

## Desenvolvimento

### Padrões de Código

- Uma classe pública por arquivo
- 100% type hints
- Docstrings no estilo Google
- Formatação com black + isort
- Linting com ruff

### Sprints de Desenvolvimento

O projeto segue um plano de 14 sprints, cada um focado em uma funcionalidade específica:

- **Sprint 00**: Fundações (janela, FPS, dependências)
- **Sprint 01**: Pipeline de assets IA
- **Sprint 02**: Sistema de cartas e deck
- **Sprint 03**: Layout básico de combate
- **Sprint 04**: Mecânicas de energia e jogabilidade
- **Sprint 05**: Sistema de intents dos inimigos
- **Sprint 06**: Mapa linear e recompensas
- **Sprint 07**: Save/Load e opções
- **Sprints 08-14**: Conteúdo, balanceamento e polimento

## Status Atual

🟢 **Sprint 00 - Foundations**: ✅ Completo
- ✔ Estrutura de diretórios
- ✔ Dependências Poetry configuradas  
- ✔ Janela 3440x1440 com contador FPS
- ✔ Loop principal básico
- ✔ Script de geração de assets (placeholder)
- ✔ Testes básicos
- ✔ CI workflow configurado

🟢 **Sprint 01 - Pipeline de Assets**: ✅ Completo
- ✔ AssetGenerator wrapper implementado
- ✔ Sistema de cache baseado em hash (MD5)
- ✔ Prompts determinísticos (seed=42)
- ✔ Arquivo prompts.yaml configurado
- ✔ Arena background (3440x1440) gerada
- ✔ Card frame (512x768) gerada
- ✔ Knight sprite sheets (5120x512) geradas
- ✔ Goblin sprite sheets (4200x420) geradas
- ✔ Testes do pipeline passando (8/8)

### Como Testar Sprint 01

1. **Gerar Assets**:
```bash
conda activate medieval-deck
python scripts/gen_assets.py
```

2. **Executar Testes**:
```bash
python -m pytest tests/test_sprint01.py -v
```

3. **Verificar Assets Gerados**:
- `assets/bg/arena.png` - Background ultrawide (3440x1440)
- `assets/ui/card_frame.png` - Moldura de carta (512x768)
- `assets/sheets/knight_idle.png` - Sprite sheet cavaleiro parado (5120x512)
- `assets/sheets/knight_attack.png` - Sprite sheet cavaleiro atacando (5120x512)
- `assets/sheets/goblin_idle.png` - Sprite sheet goblin parado (4200x420)
- `assets/sheets/goblin_attack.png` - Sprite sheet goblin atacando (4200x420)

**Resultado esperado Sprint 01**: Todos os assets são gerados como placeholders. O sistema de cache evita regeneração desnecessária. Para arte IA real, instale PyTorch + Diffusers.

## Licença

Este projeto é desenvolvido para fins educacionais e demonstração de técnicas de desenvolvimento de jogos com Python.
