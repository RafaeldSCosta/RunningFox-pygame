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

    def obter_obstaculo_da_linha(self, linha):
        """Retorna os frames e o tamanho do obstáculo de uma linha.

        O obstáculo depende da fase atual e do índice da linha.
        Retorna None quando a linha não possui um obstáculo conhecido.
        """
        if self.fases.fase == 1:
            if linha in (2, 5):
                return (
                    self.inimigos.jacare_frames,
                    self.inimigos.tamanho_jacare,
                )
            if linha in (0, 3):
                return (
                    self.inimigos.feno_frames,
                    self.inimigos.tamanho_feno,
                )
            if linha in (1, 4):
                return (
                    self.inimigos.cobra_frames,
                    self.inimigos.tamanho_cobra,
                )

        elif self.fases.fase == 2:
            if linha == 0:
                return (
                    self.inimigos.ratazana_frames,
                    self.inimigos.tamanho_ratazana,
                )
            if linha == 1:
                return (
                    self.inimigos.esc_frames,
                    self.inimigos.tamanho_esc,
                )
            if linha == 2:
                return (
                    self.inimigos.cobra_frames,
                    self.inimigos.tamanho_cobra,
                )

        return None

    def desenhar_plataformas(self):
        """Desenha os obstáculos móveis da fase atual."""
        if self.fases.fase == 1:
            y_posicoes = self.fases.y_posicoes_fase1
        else:
            y_posicoes = self.fases.y_posicoes_fase2

        self.tempo_animacao += self.vel_animacao
        if self.tempo_animacao >= 1:
            self.indice_animacao = (
                self.indice_animacao + 1
            ) % max(1, len(self.inimigos.cobra_frames))
            self.tempo_animacao = 0

        for linha, xs in enumerate(
            self.fases.linhas_das_plataformas
        ):
            if linha >= len(y_posicoes):
                break

            obstaculo = self.obter_obstaculo_da_linha(linha)
            if obstaculo is None:
                continue

            frames, tamanho = obstaculo
            imagem = frames[self.indice_animacao % len(frames)]
            y = y_posicoes[linha]

            for x in xs:
                rect = imagem.get_rect(
                    center=(x + tamanho[0] // 2, y)
                )
                self.janela.blit(imagem, rect)
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
        """Verifica se a raposa colidiu com algum obstáculo."""
        raposa_rect = pg.Rect(
            int(self.raposa.pos_raposa[0]),
            int(
                self.raposa.pos_raposa[1]
                + self.raposa.ajuste_y_raposa
            ),
            int(self.raposa.tamanho_raposa[0]),
            int(self.raposa.tamanho_raposa[1]),
        )

        if self.fases.fase == 1:
            y_posicoes = self.fases.y_posicoes_fase1
        else:
            y_posicoes = self.fases.y_posicoes_fase2

        for linha, xs in enumerate(
            self.fases.linhas_das_plataformas
        ):
            if linha >= len(y_posicoes):
                break

            obstaculo = self.obter_obstaculo_da_linha(linha)
            if obstaculo is None:
                continue

            _, tamanho = obstaculo
            y_plataforma = y_posicoes[linha]

            for x in xs:
                obstaculo_rect = pg.Rect(
                    int(x),
                    int(y_plataforma - tamanho[1] // 2),
                    *tamanho,
                )

                if raposa_rect.colliderect(obstaculo_rect):
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
