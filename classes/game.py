import pygame as pg
from sys import exit
from classes.player import Raposa
from classes.enemies import Inimigos
from classes.levels import Fases


"""
Módulo de gerenciamento do jogo - Cruzamento da Fazenda.

Contém a classe `CruzamentoFazenda` que inicializa a janela do Pygame,
carrega recursos (fundo, sprites via outras classes) e contém métodos
para desenhar e atualizar plataformas, detectar colisões e reagir aos
eventos do jogo (por exemplo, chegada à fazenda ou aos ovos).

Comentários em português explicam a finalidade de cada método e os
trechos de lógica mais importantes.
"""


class CruzamentoFazenda:
    """Classe principal que gerencia a tela e a lógica básica do jogo.

    A classe agrega objetos das classes `Raposa`, `Inimigos` e `Fases`.
    Ela não é um loop principal completo por si só (presumivelmente existe
    em `main.py`), mas fornece utilitários para desenhar, atualizar e
    verificar colisões.
    """

    def __init__(self):
        # Inicialização do Pygame e janela principal
        pg.init()
        self.janela = pg.display.set_mode((950, 880))
        pg.display.set_caption("Cruzamento da Fazenda")
        self.relogio = pg.time.Clock()

        # Carrega imagem de fundo; em caso de erro encerra o jogo
        try:
            # --- Fundo inicial ---
            self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda.png").convert()
            self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))
        except Exception as e:
            # Falha ao carregar assets é crítica aqui — imprimimos o erro
            # e saímos para evitar estados inconsistentes.
            print("❌ ERRO ao carregar imagens:", e)
            pg.quit()
            exit()

        # --- Componentes principais ---
        # Instanciamos os objetos que gerenciam jogador, inimigos e fases
        self.raposa = Raposa()
        self.inimigos = Inimigos()
        self.fases = Fases()

        # --- parâmetros gerais ---
        # Contadores e flags usados por vários métodos
        self.vidas = 3
        self.game_over = False
        self.indice_animacao = 0
        self.tempo_animacao = 0.0
        self.vel_animacao = 0.20
        self.reached_ovos = False

    # -------------------------------------------------------------
    def limpar_janela(self):
        """Redesenha o fundo na janela.

        Chamado no início do ciclo de desenho para limpar a tela e
        preparar o próximo frame.
        """
        self.janela.blit(self.fundo_imagem, (0, 0))

    # -------------------------------------------------------------
    def desenhar_plataformas(self):
        """Desenha plataformas/inimigos móveis conforme a fase atual.

        - Seleciona as posições Y corretas dependendo da fase (1 ou 2).
        - Atualiza o índice de animação com base em `tempo_animacao`.
        - Para cada plataforma (cada x em cada linha) escolhe qual
          sprite desenhar (jacaré, ratazana, feno, escorpião, cobra)
          de acordo com a linha e a fase.
        """
        y_posicoes = self.fases.y_posicoes_fase1 if self.fases.fase == 1 else self.fases.y_posicoes_fase2

        # Avança o temporizador de animação e atualiza o índice quando chega a 1
        self.tempo_animacao += self.vel_animacao
        if self.tempo_animacao >= 1:
            # Uso de max(1, ...) para evitar divisão por zero caso não hajam frames
            self.indice_animacao = (self.indice_animacao + 1) % max(1, len(self.inimigos.cobra_frames))
            self.tempo_animacao = 0

        # Percorre cada linha de plataformas (linhas_das_plataformas é uma lista de listas de Xs)
        for linha, xs in enumerate(self.fases.linhas_das_plataformas):
            if linha >= len(y_posicoes):
                # Se não houver uma posição Y definida para esta linha, paramos
                break
            y = y_posicoes[linha]
            for x in xs:
                # Determina e desenha a imagem apropriada para a linha/fase
                # Jacarés (fase 1) / Ratazanas (fase 2)
                if (self.fases.fase == 1 and linha in (2, 5)):
                    img = self.inimigos.jacare_frames[self.indice_animacao % len(self.inimigos.jacare_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_jacare[0] // 2, y))
                    self.janela.blit(img, rect)
                elif (self.fases.fase == 2 and linha == 0):
                    img = self.inimigos.ratazana_frames[self.indice_animacao % len(self.inimigos.ratazana_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_ratazana[0] // 2, y))
                    self.janela.blit(img, rect)

                # Fenos (fase 1) / Escorpiões (fase 2)
                elif (self.fases.fase == 1 and linha in (0, 3)):
                    img = self.inimigos.feno_frames[self.indice_animacao % len(self.inimigos.feno_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_feno[0] // 2, y))
                    self.janela.blit(img, rect)
                elif (self.fases.fase == 2 and linha == 1):
                    img = self.inimigos.esc_frames[self.indice_animacao % len(self.inimigos.esc_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_esc[0] // 2, y))
                    self.janela.blit(img, rect)

                # Cobras (ambas fases)
                elif (self.fases.fase == 1 and linha in (1, 4)) or (self.fases.fase == 2 and linha == 2):
                    img = self.inimigos.cobra_frames[self.indice_animacao % len(self.inimigos.cobra_frames)]
                    rect = img.get_rect(center=(x + self.inimigos.tamanho_cobra[0] // 2, y))
                    self.janela.blit(img, rect)

    # -------------------------------------------------------------
    def atualizar_plataformas(self):
        """Atualiza as posições X das plataformas/inimigos móveis.

        Lógica por linha:
        - Linhas 2 e 5: jacarés/ratazanas se movem para a direita.
        - Linhas 0 e 3: fenos/escorpiões se movem para a esquerda.
        - Linhas 1 e 4: cobras se movem para a direita com velocidade diferente.

        Quando uma plataforma sai da tela, ela é reposicionada no lado
        oposto (efeito loop), usando valores limites adequados a cada tipo.
        """
        for y in range(len(self.fases.linhas_das_plataformas)):
            for i in range(len(self.fases.linhas_das_plataformas[y])):
                if y in (2, 5):  # jacarés / ratazanas
                    self.fases.linhas_das_plataformas[y][i] += 1 + self.fases.v_dif
                    if self.fases.linhas_das_plataformas[y][i] > 880:
                        self.fases.linhas_das_plataformas[y][i] = -100
                elif y in (0, 3):  # fenos / escorpiões
                    self.fases.linhas_das_plataformas[y][i] -= 2 + self.fases.v_dif
                    if self.fases.linhas_das_plataformas[y][i] < -120:
                        self.fases.linhas_das_plataformas[y][i] = 880
                elif y in (1, 4):  # cobras
                    self.fases.linhas_das_plataformas[y][i] += 1.5 + self.fases.v_dif
                    if self.fases.linhas_das_plataformas[y][i] > 950:
                        self.fases.linhas_das_plataformas[y][i] = -300

    # -------------------------------------------------------------
    def raposa_colidiu_com_objeto(self):
        """Verifica se a raposa colidiu com alguma plataforma/inimigo.

        - Constrói um Rect da raposa usando posição e ajuste vertical.
        - Para cada plataforma visível, constrói um rect correspondente
          com base no tipo (usa os tamanhos em `self.inimigos`).
        - Se houver interseção (`colliderect`) retorna True, caso contrário False.
        """
        raposa_rect = pg.Rect(int(self.raposa.pos_raposa[0]), int(self.raposa.pos_raposa[1] + self.raposa.ajuste_y_raposa),
                              int(self.raposa.tamanho_raposa[0]), int(self.raposa.tamanho_raposa[1]))
        y_posicoes = self.fases.y_posicoes_fase1 if self.fases.fase == 1 else self.fases.y_posicoes_fase2
        for linha, xs in enumerate(self.fases.linhas_das_plataformas):
            if linha >= len(y_posicoes):
                break
            y_plat = y_posicoes[linha]
            for x in xs:
                # Cria rects diferentes dependendo do tipo de plataforma
                if (self.fases.fase == 1 and linha in (2, 5)):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_jacare[1] // 2), *self.inimigos.tamanho_jacare)
                elif (self.fases.fase == 2 and linha == 0):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_ratazana[1] // 2), *self.inimigos.tamanho_ratazana)
                elif (self.fases.fase == 1 and linha in (0, 3)) or (self.fases.fase == 2 and linha == 1):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_feno[1] // 2), *self.inimigos.tamanho_feno)
                elif (self.fases.fase == 1 and linha in (1, 4)) or (self.fases.fase == 2 and linha == 2):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.inimigos.tamanho_cobra[1] // 2), *self.inimigos.tamanho_cobra)
                else:
                    # Linha não mapeada para plataformas relevantes
                    continue
                if raposa_rect.colliderect(plat_rect):
                    return True
        return False

    # -------------------------------------------------------------
    def resetar_posicao_raposa(self, colisao=False):
        """Reseta a posição da raposa para o ponto inicial.

        Se `colisao` for True, decrementa vidas, checa game over e imprime
        um log simples. Depois reposiciona a raposa e seu sprite frontal.
        """
        if colisao:
            self.vidas -= 1
            if self.vidas < 0:
                self.vidas = 0
            print(f"💥 Colidiu! Vidas restantes: {self.vidas}")
            if self.vidas == 0:
                self.game_over = True
        # Posição inicial definida por coord x,y
        self.raposa.pos_raposa = [370, 760]
        self.raposa.sprite_raposa_atual = self.raposa.sprite_frente

    # -------------------------------------------------------------
    def tratar_colisao_com_obstaculo(self):
        if self.raposa_colidiu_com_objeto():
            self.resetar_posicao_raposa(colisao=True)


    # Checa se chegou na fazenda (área de chegada) e avança de fase
    def verificar_avanco_de_fase(self, raposa_rect):
        if raposa_rect.colliderect(self.fases.area_fazenda):
            print("🐾 A raposa chegou na fazenda!")

            self.fases.proxima_fase()

            # Troca o fundo para o segundo (fase 2) e escala
            self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda_2.png").convert()
            self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))
            self.resetar_posicao_raposa()

    # Checa área dos ovos (condição adicional: area_ovos.width > 1 evita áreas vazias)
    def verificar_vitoria(self, raposa_rect):
        if self.fases.area_ovos and self.fases.area_ovos.width > 1 and raposa_rect.colliderect(self.fases.area_ovos):
            if not self.reached_ovos:
                print("🐾 A raposa chegou nos ovos!")
                self.reached_ovos = True
                self.game_over = True

    def checar_colisoes_e_reagir(self):
        """Coordena as diferentes reações às colisões."""
        if self.game_over:
            return

        self.tratar_colisao_com_obstaculo()

        raposa_rect = pg.Rect(
            int(self.raposa.pos_raposa[0]),
            int(
                self.raposa.pos_raposa[1]
                + self.raposa.ajuste_y_raposa
            ),
            int(self.raposa.tamanho_raposa[0]),
            int(self.raposa.tamanho_raposa[1])
        )

        self.verificar_avanco_de_fase(raposa_rect)
        self.verificar_vitoria(raposa_rect)
