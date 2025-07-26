# 🏰 Medieval Deck - Roadmap Completo dos Sprints

**AI-Generated Roguelike Card Game • 3440x1440 Ultrawide • RTX 5070 Optimized**

---

## ✅ **Sprint 00 - Foundation (COMPLETE)**
*Duração: 1 dia • Status: 100% Entregue*

### Objetivos:
- [x] Ferramental pronto, janela vazia com FPS
- [x] Configuração inicial do projeto
- [x] Ambiente de desenvolvimento
- [x] Pipeline CI/CD

### Entregáveis:
- [x] Poetry init + deps do prompt principal
- [x] Workflow GitHub Actions (lint, type, tests)
- [x] src/main.py abre janela 3440×1440, mostra FPS contador
- [x] Janela abre sem erros
- [x] README "Como rodar"
- [x] Estrutura de diretórios organizada

### Aceite:
- [x] ✔ CI verde ✔ Janela abre sem erros ✔ README "Como rodar"

---

## ✅ **Sprint 01 - Pipeline de Assets (COMPLETE)**
*Duração: 2 dias • Status: 100% Entregue*

### Objetivos:
- [x] scripts/gen_assets.py gera arena.png, card_frame.png, knight_idle.png
- [x] Pipeline de geração AI com Stable Diffusion XL
- [x] Assets visuais core do jogo
- [x] Otimização para RTX 5070

### Entregáveis:
- [x] Implementar AssetGenerator wrapper
- [x] prompts.yaml com 3+ prompts iniciais
- [x] Função hash(prompt+seed) → skip se cache
- [x] Teste tests/test_assets_exist.py
- [x] **SDXL Pipeline**: PyTorch 2.7.0 + CUDA 12.8 + XFormers 0.0.30
- [x] **Backgrounds (3440x1440)**:
  - Arena de combate (`arena.png`)
  - Menu principal (`menu.png`) 
  - Tela de seleção (`card_selection.png`)
- [x] **Character Sprites**:
  - Knight idle/attack (5120x512, 10 frames cada)
  - Goblin idle/attack (4240x424, 10 frames cada)
- [x] **UI Elements**:
  - Card frame medieval (`card_frame.png`)

### Aceite:
- [x] ✔ Arquivos gerados ✔ Teste passa ✔ README atualizado

---

## ✅ **Sprint 02 - UI & Game Flow (COMPLETE)**
*Duração: 2 dias • Status: 100% Entregue*

### Objetivos:
- [x] Sistema de navegação entre telas
- [x] Fluxo de jogo completo
- [x] Transitions e polish visual
- [x] Arquitetura escalável

### Entregáveis:
- [x] **Screen Management System**:
  - ScreenManager com stack de telas
  - ScreenBase com fade transitions (500ms)
  - Navegação fluida entre estados
- [x] **Telas Implementadas**:
  - MenuScreen com background AI
  - CharacterSelectScreen com blur effects
  - CombatScreen com arena AI
  - ResultScreen com auto-return
- [x] **Game Flow**: Menu → Selection → Combat → Result → Menu
- [x] **Combat Básico**: Knight vs Goblin com health bars
- [x] **Testing Suite**: 21/21 testes passando
- [x] **Resource System**: Loading com cache otimizado

---

## ✅ **Sprint 03 - Card Game Mechanics (COMPLETE)**
*Duração: 3-4 dias • Status: 100% Entregue*

### Objetivos:
- [x] Card & Deck Model - Regras básicas de cartas, deck e mão
- [x] Sistema de cartas e deck building expandido
- [x] Mecânicas de combate por turnos melhoradas
- [x] CombatScreen "Skeleton" - Layout visual com mecânica
- [x] UI interativa e responsiva

### Entregáveis:
- [x] **Card System Expandido**:
  - game.cards.Card dataclass com tipos (Attack, Skill, Power, Special)
  - Deck de 30 cartas balanceadas para Knight
  - Sistema de raridade (Common, Uncommon, Rare)
  - Cores por tipo para identificação visual
- [x] **Combat Engine Completo**:
  - Sistema de energia expandido com power effects
  - Integração completa com tipos de carta
  - Efeitos especiais: multi-hit, card draw, energy gain
  - Power cards com efeitos permanentes
- [x] **Deck Management Avançado**:
  - game.deck.Deck com reshuffle automático
  - Hand management com draw/discard
  - Cobertura 90%+ em testes
- [x] **CombatScreen Interativo**:
  - UI com cartas reais (não placeholder)
  - Sistema de hover e seleção de cartas
  - HUD energia/HP/Block em tempo real
  - Feedback visual de ações
- [x] **Mecânica de Energia & Jogar Carta**:
  - CombatEngine.play_card() aplica todos efeitos
  - Sistema de turnos: Player → Enemy → Repeat
  - Condições de vitória/derrota funcionais
- [x] **Testing Suite**: 9/9 testes específicos do Sprint 03
  - Partícula simples ao causar dano
  - Testes integração: Strike reduz HP goblin
- [ ] **Character Classes**:
  - Mage sprites (SDXL geração)
  - Archer sprites (SDXL geração)
  - Habilidades únicas por classe

### Aceite (Sprint 03):
- [x] ✔ Cobertura 90% em deck + cards ✔ pytest green
- [ ] ✔ FPS >55 ✔ Cartas renderizadas ✔ Nenhum placeholder cobre HUD
- [ ] ✔ Jogar Guard cria Block ✔ After EndTurn, Block zera

---

## 🔄 **Sprint 04 - Enemy AI & Intent System (PLANEJADO)**
*Duração: 2-3 dias*

### Objetivos:
- [ ] Sistema de Intents do Inimigo
- [ ] Inimigo telegrafa ação com ícone e valor
- [ ] Múltiplos tipos de inimigos
- [ ] Balanceamento avançado

### Entregáveis Planejados:
- [ ] **Enemy Intent System**:
  - enemy.Intent Enum ("attack","defend","buff","heal","debuff")
  - Enemy sorteia intent a cada turno
  - Render ícone + número acima do sprite
  - CombatEngine.enemy_turn() usa intent
- [ ] **Enemy Variety**:
  - Skeleton sprites (SDXL geração)
  - Orc sprites (SDXL geração)
  - Diferentes padrões de IA
- [ ] **Combat Polish**:
  - Partículas de dano
  - Animações de ataque/defesa
  - Sound effects básicos

### Aceite:
- [ ] ✔ Ícone troca todo turno ✔ Dano calculado corretamente

---

## 🔄 **Sprint 05 - Progression & Map System (PLANEJADO)**
*Duração: 3-4 dias*

### Objetivos:
- [ ] MapScreen Linear + Recompensa
- [ ] Progredir em 8 nós e ganhar carta
- [ ] Sistema de progressão
- [ ] Save/Load system

### Entregáveis Planejados:
- [ ] **Map & Progression**:
  - ui.map_screen lista 8 retângulos clicáveis
  - Após vitória → RewardScreen (3 cartas aleatórias)
  - Escolher carta adiciona ao deck → retorna ao mapa
- [ ] **Persistence**:
  - GameState serializa em JSON (saves/run.json)
  - ESC abre overlay: Resume / Save / Quit
  - Save/load game state
  - Profile management
- [ ] **Settings**:
  - Opções: volume slider, toggle fullscreen
  - Settings persistence

### Aceite:
- [ ] ✔ Deck cresce ✔ Pointers de nós avançam
- [ ] ✔ Salvar e reabrir continua no mesmo nó

---

## 🔄 **Sprint 06 - Content Expansion A (PLANEJADO)**
*Duração: 2-3 dias*

### Objetivos:
- [ ] Conteúdo A (12 cartas + Skeleton & Orc)
- [ ] Aumentar variedade de gameplay
- [ ] Mini-boss Dark Wizard

### Entregáveis Planejados:
- [ ] **Card Expansion**:
  - Gerar 12 artes de carta novas via SDXL
  - 60+ cartas únicas balanceadas
  - Balancear custos e valores
- [ ] **Enemy Expansion**:
  - Gerar sprite-sheet skeleton_idle/attack & orc_idle/attack
  - 8-10 inimigos diferentes
- [ ] **Mini-Boss System**:
  - Generate wizard sheets + BG torre sombria
  - Intents: Flame 8, Shield 6, Weak 2
  - Boss encounters com mecânicas únicas

### Aceite:
- [ ] ✔ Todas cartas novas funcionam em combate
- [ ] ✔ Batalha vence → tela "Act Clear"

---

## 🔄 **Sprint 07 - Audio & VFX Polish (PLANEJADO)**
*Duração: 2-3 dias*

### Objetivos:
- [ ] Audio & VFX Pass
- [ ] Trilha de fundo, SFX e partículas polidas
- [ ] UX & Acessibilidade

### Entregáveis Planejados:
- [ ] **Audio System**:
  - Música loop na arena
  - SFX strike / guard / heal
  - Música de boss (ogg loop)
  - Sonoridade nivelada -12 LUFS
- [ ] **Visual Effects**:
  - ParticleEmitter sparks (blend add)
  - Câmera shake (8 px) em ataques críticos
  - Animations melhoradas
- [ ] **Accessibility**:
  - Palette alternativa (daltonismo) trigger via opções
  - Hover tooltip mostra texto da carta ampliado
  - pygame.joystick mapeia D-pad para selecionar carta

### Aceite:
- [ ] ✔ CPU < 5% extra
- [ ] ✔ Cartas selecionáveis apenas via controle

---

## 🔄 **Sprint 08 - Final Boss & Victory (PLANEJADO)**
*Duração: 2-3 dias*

### Objetivos:
- [ ] Boss Dragão + Tela de Vitória
- [ ] Combate final épico
- [ ] Balance & QA Hardening

### Entregáveis Planejados:
- [ ] **Final Boss**:
  - Sprite-sheet dragon (4 poses) + BG caverna
  - 4-fase pattern: Flame 14 / Buff 3 Str / Swipe 10×2 / Rest
  - Tela "You Win" e stats da run
- [ ] **Quality Assurance**:
  - Playtest 50 runs, coletar dados dmg recebido
  - Ajustar cartas overpower/underpower
  - Profiler: eliminar allocs na draw()
  - Atualizar docs + type hints faltantes
- [ ] **Build & Distribution**:
  - Criar spec PyInstaller one-folder
  - Headless stress-test 500 combats (pytest-param)
  - dist/medieval-deck.exe abre, joga Ato 1 sem crash

### Aceite:
- [ ] ✔ Dragão derrota encerra run
- [ ] ✔ Avg run win ~55-60% ✔ Perf ok

---

## 🎯 **Objetivos de Longo Prazo**

### **MVP (Minimum Viable Product) - Sprint 03**
- Jogo completo jogável
- 1 personagem (Knight) funcional
- Combat básico balanceado
- Assets AI de alta qualidade

### **Full Release - Sprint 05**
- 3 personagens únicos
- 60+ cartas balanceadas
- 10+ inimigos variados
- Sistema completo de progressão
- Polish AAA-level

---

## 📊 **Métricas de Sucesso**

### **Técnicas:**
- [ ] 100% testes passando sempre
- [ ] 60+ FPS em 3440x1440
- [ ] <2GB RAM usage
- [ ] Assets <500MB total

### **Gameplay:**
- [ ] Partidas de 5-15 minutos
- [ ] Curva de dificuldade balanceada
- [ ] 3 estratégias viáveis por personagem
- [ ] Replay value alto

### **Qualidade:**
- [ ] Assets indistinguíveis de arte profissional
- [ ] UI/UX intuitiva
- [ ] Zero crashes
- [ ] Performance consistente

---

## 🛠️ **Stack Tecnológico**

### **Core:**
- Python 3.11 + Pygame
- Conda environment management
- pytest para testing

### **AI Pipeline:**
- Stable Diffusion XL
- PyTorch 2.7.0 + CUDA 12.8
- XFormers 0.0.30
- RTX 5070 optimization

### **Development:**
- VS Code + GitHub Copilot
- Git version control
- GitHub Actions CI/CD
- Type hints + documentation

---

**🏆 Medieval Deck - Roadmap completo para criar um roguelike card game AAA com AI!**
