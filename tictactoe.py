import copy
import sys
import pygame
import random
import numpy as np

# ----------------- CONSTANTES ---------------------------- 
LARGURA = 600
ALTURA = 600

LINHA = 3
COLUNAS = 3
TAMANHO_BOARD = LARGURA // COLUNAS

LINE_LARGURA = 15
O_LARGURA = 15
X_LARGURA = 20

RADIUS = TAMANHO_BOARD // 4

OFFSET = 50

COR_FUNDO = (30, 100, 180)
LINE_COLOR = (23, 145, 135)
COR_O = (240, 230, 200)
COR_X = (66, 66, 66)

#--------------------------------------------------------


# -------------------- PYGAME SETUP ---------------------

pygame.init()
screen = pygame.display.set_mode( (LARGURA, ALTURA) )
pygame.display.set_caption('DEASFIO JOGO DA VELHA')
screen.fill( COR_FUNDO )

# --------------- CLASSES -----------------------------

class Board:

    def __init__(self):
        self.squares = np.zeros( (LINHA, COLUNAS) )
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):

        # VITÓRIA NA VERTICAL
        for col in range(COLUNAS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = COR_O if self.squares[0][col] == 2 else COR_X
                    iPos = (col * TAMANHO_BOARD + TAMANHO_BOARD // 2, 20)
                    fPos = (col * TAMANHO_BOARD + TAMANHO_BOARD // 2, ALTURA - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_LARGURA)
                return self.squares[0][col]

        # VITÓRIA NA HORIZONTAL
        for row in range(LINHA):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = COR_O if self.squares[row][0] == 2 else COR_X
                    iPos = (20, row * TAMANHO_BOARD + TAMANHO_BOARD // 2)
                    fPos = (LARGURA - 20, row * TAMANHO_BOARD + TAMANHO_BOARD // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_LARGURA)
                return self.squares[row][0]

        # VITÓRIA NA DIAGONAL 1
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = COR_O if self.squares[1][1] == 2 else COR_X
                iPos = (20, 20)
                fPos = (LARGURA - 20, ALTURA - 20)
                pygame.draw.line(screen, color, iPos, fPos, X_LARGURA)
            return self.squares[1][1]

        # VITÓRIA NA DIAGONAL 2
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = COR_O if self.squares[1][1] == 2 else COR_X
                iPos = (20, ALTURA - 20)
                fPos = (LARGURA - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, X_LARGURA)
            return self.squares[1][1]

        # SEM VITÓRIAS
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(LINHA):
            for col in range(COLUNAS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

# JOGANDO CONTRA A MÁQUINA

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # ---------------------------- RANDOM -----------------------------

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    # ------------------------------- MINIMAX ------------------------

    def minimax(self, board, maximizing):
        
        # TERMINAL
        case = board.final_state()

        # VITÓRIA JOGADOR 1
        if case == 1:
            return 1, None

        # VITÓRIA JOGADOR 2
        if case == 2:
            return -1, None

        # EMPATE
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MAIN EVAL --- (analisa o argumento da expressão e o avalia como uma expressão python)

    def eval(self, main_board):
        if self.level == 0:
            # RANDOM
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # MINIMAX
            eval, move = self.minimax(main_board, False)

        print(f'Posição {move} expressão: {eval}')

        return move

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # DEFINIR PLAYER 
        self.gamemode = 'ai' # 1V1 OU 1XMÁQUINA
        self.running = True
        self.show_lines()

    # -------------------------------- DESENHOS ------------------------------

    def show_lines(self):
        screen.fill( COR_FUNDO )

        # VERTICAL
        pygame.draw.line(screen, LINE_COLOR, (TAMANHO_BOARD, 0), (TAMANHO_BOARD, ALTURA), LINE_LARGURA)
        pygame.draw.line(screen, LINE_COLOR, (LARGURA - TAMANHO_BOARD, 0), (LARGURA - TAMANHO_BOARD, ALTURA), LINE_LARGURA)

        # HORIZONTAL
        pygame.draw.line(screen, LINE_COLOR, (0, TAMANHO_BOARD), (LARGURA, TAMANHO_BOARD), LINE_LARGURA)
        pygame.draw.line(screen, LINE_COLOR, (0, ALTURA - TAMANHO_BOARD), (LARGURA, ALTURA - TAMANHO_BOARD), LINE_LARGURA)

    def draw_fig(self, row, col):
        if self.player == 1:
            # DESENAH X
            # LINHA
            start_desc = (col * TAMANHO_BOARD + OFFSET, row * TAMANHO_BOARD + OFFSET)
            end_desc = (col * TAMANHO_BOARD + TAMANHO_BOARD - OFFSET, row * TAMANHO_BOARD + TAMANHO_BOARD - OFFSET)
            pygame.draw.line(screen, COR_X, start_desc, end_desc, X_LARGURA)
            # LINHA
            start_asc = (col * TAMANHO_BOARD + OFFSET, row * TAMANHO_BOARD + TAMANHO_BOARD - OFFSET)
            end_asc = (col * TAMANHO_BOARD + TAMANHO_BOARD - OFFSET, row * TAMANHO_BOARD + OFFSET)
            pygame.draw.line(screen, COR_X, start_asc, end_asc, X_LARGURA)
        
        elif self.player == 2:
            # DESENHA BOLINHA
            center = (col * TAMANHO_BOARD + TAMANHO_BOARD // 2, row * TAMANHO_BOARD + TAMANHO_BOARD // 2)
            pygame.draw.circle(screen, COR_O, center, RADIUS, O_LARGURA)

    # ----------------------- OUTROS MÉTODOS -----------------------------------

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # ---------------------------------- OBJECTS ---------------------------------

    game = Game()
    board = game.board
    ai = game.ai

    # ----------------------------------- PROGRAMA PRINCIPAL --------------------------------

    while True:
        
        # PYGAME
        for event in pygame.event.get():

            # SAIR
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # MODO DE JOGO
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # REINICIAR
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # LEVEL 1 AI
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # LEVEL 2 AI
                if event.key == pygame.K_1:
                    ai.level = 1

            # MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // TAMANHO_BOARD
                col = pos[0] // TAMANHO_BOARD
                
                # JOGADA PLAYER
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False


        # AI 
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # TELA
            pygame.display.update()

            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()
