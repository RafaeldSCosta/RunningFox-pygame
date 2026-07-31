# 🦊 Running Fox

> Um jogo estilo *Crossy Road* desenvolvido em Python com a biblioteca Pygame.

---

## 👥 Integrantes do Grupo

* **Julia Mendes**
* **Livia Pinheiro**
* **Rafael dos Santos**

---

## 🎮 Sobre o Jogo

**Running Fox** é um jogo do gênero *"crossy road"* onde você controla uma raposa que deve fugir de vários inimigos. O objetivo principal é pegar os ovos no celeiro no menor tempo possível, mantendo suas vidas intactas para entrar no ranking de pontuações.

### 📺 Demonstração em Vídeo
Confira o funcionamento completo das fases e mecânicas no YouTube:
* **Link:** [Assistir à demonstração do Running Fox](https://youtu.be/3nlJiPyZyPI)

---

## 🕹️ Como Jogar

| Tecla | Comando / Ação |
| :---: | :--- |
| **`↑` (Cima)** | Mover-se para frente *(único movimento que emite som)* |
| **`←` / `→`** | Movimentação lateral (esquerda / direita) |
| **`R`** | Reiniciar a fase atual |
| **`Q`** | Sair para o menu principal |

---

## ⚙️ Mecânica Principal

* **Objetivo:** Evite colisões com obstáculos e inimigos e tente terminar com todas as vidas para vencer a fase.
* **Ação:** A raposa deve atravessar a fase desviando dos perigos pelo caminho.
* **Áudio & Imersão:** O jogo é sincronizado com uma trilha sonora, criando ritmo e imersão.
* **Progressão:** A cada fase, a dificuldade e a velocidade aumentam.
* **Derrota (Game Over):** Se perder todas as vidas → Game Over.
* **Vitória:** Ao alcançar os ovos no final → Vitória e entrada no ranking.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* [Python 3.8+](https://www.python.org/) instalado no computador.
* Biblioteca **Pygame** instalada.

### Passo a Passo

1. **Clone o repositório:**
    git clone [https://github.com/SEU-USUARIO/RunningFox--Pygame.git](https://github.com/SEU-USUARIO/RunningFox--Pygame.git)
    cd RunningFox--Pygame

2. **Instale as dependências:**
    pip install pygame

3. **Execute o jogo:**
    python main.py

---

## 📂 Estrutura do Projeto

    RunningFox--Pygame/
    │
    ├── main.py                 # Script principal: gerencia o loop do jogo e os estados (menu, jogo, end)
    ├── audio.py                # Carrega e inicializa sons e músicas do jogo
    ├── ranking.py              # Sistema de ranking (salva e mostra pontuações em JSON)
    ├── screens.py              # Gerencia telas (Start, Level, End) e transições
    ├── scores.json             # Arquivo JSON para salvar o ranking de jogadores
    │
    ├── classes/                # Contém as classes principais do jogo
    │   ├── game.py             # Classe principal do jogo (CruzamentoFazenda): lógica e fases
    │   ├── hud.py              # Classe HUD: interface gráfica (vidas, cronômetro, etc.)
    │   ├── player.py           # Classe da raposa (personagem jogável)
    │   ├── enemies.py          # Classes de inimigos e obstáculos
    │   └── levels.py           # Configuração e controle das fases do jogo
    │
    ├── imagens_pygame/         # Recursos visuais do jogo (sprites, fundos, botões)
    │   ├── imagem_start.png    # Tela inicial
    │   ├── instru.png          # Tela de instruções
    │   ├── level_1.png         # Tela de início da fase 1
    │   ├── level_2.png         # Tela de início da fase 2
    │   ├── titulo.png          # Logo do jogo (Running Fox)
    │   ├── win.png             # Tela de vitória
    │   ├── game_over.png       # Tela de derrota
    │   ├── ranking.png         # Tela de ranking
    │   ├── botao_start.png     # Imagem do botão de iniciar
    │   ├── fundo_fazenda.png   # Fundo do cenário principal
    │   ├── nuvem1.png...       # Sprites das nuvens do menu
    │   ├── frente.png...       # Sprites da raposa (costas/frente)
    │   ├── feno1.png...        # Sprites dos obstáculos
    │   └── rat1.png...         # Sprites dos inimigos
    │
    └── sons/                   # Recursos de áudio (efeitos e trilhas sonoras)
        ├── start.mp3           # Som ao iniciar o jogo
        ├── fases.mp3           # Som de transição entre fases
        ├── trilha.mp3          # Trilha sonora principal
        ├── raposa.mp3          # Som da raposa se movendo
        └── game_over.mp3       # Som de derrota

---

## 📄 Licença

Este projeto foi desenvolvido com fins educacionais.
