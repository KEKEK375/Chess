import pygame


class Piece:
    def __init__(self, colour: str, type: str, img, scale: int):
        self.colour = colour
        self.type = type
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (scale, scale))

        # for pawns
        if self.type == "pawn":
            self.is_enpassantable = False
            self.can_enpassant = False

        # for rooks and kings
        if self.type == "rook" or self.type == "king" or "pawn":
            self.has_moved = False


class Game:
    def __init__(self, size: int = 512):
        ## CONSTANTS ##
        self.WIDTH = self.HEIGHT = size
        self.SQUARE_SIZE = self.WIDTH // 8

        ## COLOURS ##
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.OFF_WHITE = (235, 235, 235)
        self.GREEN = (30, 130, 49)
        self.RED = (173, 19, 19)
        self.YELLOW = (230, 223, 41)
        self.DARK_YELLOW = (220, 215, 38)

        ## VARIABLES ##
        self.selected_tile = None
        self.current_player = "white"
        self.possible_moves = []

        pygame.init()

        self.set_screen()
        self.create_board()
        self.populate_board()
        self.draw_board()

        # for debugging and testing
        # self.test()

        self.run()

    def set_screen(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess")

    def create_board(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def populate_board(self):
        # pawns
        for col in range(len(self.board)):
            self.board[1][col] = Piece(
                "black", "pawn", "images/black_pawn.png", self.SQUARE_SIZE
            )
        for col in range(len(self.board)):
            self.board[6][col] = Piece(
                "white", "pawn", "images/white_pawn.png", self.SQUARE_SIZE
            )
        # rooks
        self.board[0][0] = Piece(
            "black", "rook", "images/black_rook.png", self.SQUARE_SIZE
        )
        self.board[0][7] = Piece(
            "black", "rook", "images/black_rook.png", self.SQUARE_SIZE
        )
        self.board[7][0] = Piece(
            "white", "rook", "images/white_rook.png", self.SQUARE_SIZE
        )
        self.board[7][7] = Piece(
            "white", "rook", "images/white_rook.png", self.SQUARE_SIZE
        )
        # knights
        self.board[0][1] = Piece(
            "black", "knight", "images/black_knight.png", self.SQUARE_SIZE
        )
        self.board[0][6] = Piece(
            "black", "knight", "images/black_knight.png", self.SQUARE_SIZE
        )
        self.board[7][1] = Piece(
            "white", "knight", "images/white_knight.png", self.SQUARE_SIZE
        )
        self.board[7][6] = Piece(
            "white", "knight", "images/white_knight.png", self.SQUARE_SIZE
        )
        # bishops
        self.board[0][2] = Piece(
            "black", "bishop", "images/black_bishop.png", self.SQUARE_SIZE
        )
        self.board[0][5] = Piece(
            "black", "bishop", "images/black_bishop.png", self.SQUARE_SIZE
        )
        self.board[7][2] = Piece(
            "white", "bishop", "images/white_bishop.png", self.SQUARE_SIZE
        )
        self.board[7][5] = Piece(
            "white", "bishop", "images/white_bishop.png", self.SQUARE_SIZE
        )
        # queens
        self.board[0][3] = Piece(
            "black", "queen", "images/black_queen.png", self.SQUARE_SIZE
        )
        self.board[7][3] = Piece(
            "white", "queen", "images/white_queen.png", self.SQUARE_SIZE
        )
        # kings
        self.board[0][4] = Piece(
            "black", "king", "images/black_king.png", self.SQUARE_SIZE
        )
        self.board[7][4] = Piece(
            "white", "king", "images/white_king.png", self.SQUARE_SIZE
        )

    def draw_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                # draw squares
                if (col + row) % 2 == 0:
                    colour = self.GREEN
                else:
                    colour = self.OFF_WHITE
                pygame.draw.rect(
                    self.screen,
                    colour,
                    (
                        col * self.SQUARE_SIZE,
                        row * self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                    ),
                )

                # draw selected tile
                # TODO draw as new surface to change alpha value
                if (
                    self.selected_tile is not None
                    and self.selected_tile[0] == row
                    and self.selected_tile[1] == col
                ):
                    pygame.draw.rect(
                        self.screen,
                        self.YELLOW,
                        (
                            col * self.SQUARE_SIZE,
                            row * self.SQUARE_SIZE,
                            self.SQUARE_SIZE,
                            self.SQUARE_SIZE,
                        ),
                    )

                # draw possible moves
                if (row, col) in self.possible_moves:
                    if self.does_move_take[self.possible_moves.index((row, col))]:
                        pos_colour = self.RED
                    else:
                        pos_colour = self.DARK_YELLOW
                    pygame.draw.rect(
                        self.screen,
                        pos_colour,
                        (
                            col * self.SQUARE_SIZE,
                            row * self.SQUARE_SIZE,
                            self.SQUARE_SIZE,
                            self.SQUARE_SIZE,
                        ),
                    )

                # draw pieces
                if self.board[row][col] is not None:
                    self.screen.blit(
                        self.board[row][col].image,
                        (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE),
                    )

    def toggle_current_player(self):
        if self.current_player == "white":
            self.current_player = "black"
            return
        self.current_player = "white"

    def show_possible_moves(self, piece: Piece, tile: tuple[str, str]):
        self.possible_moves = []
        self.does_move_take = []
        type = piece.type
        colour = piece.colour
        match type:
            case "pawn":
                self.show_pawn_moves(piece, tile, colour)
            case "rook":
                self.show_rook_moves(piece, tile, colour)
            case "knight":
                self.show_knight_moves(piece, tile, colour)
            case "bishop":
                self.show_bishop_moves(piece, tile, colour)
            case "queen":
                self.show_rook_moves(piece, tile, colour)
                self.show_bishop_moves(piece, tile, colour)
            case "king":
                self.show_king_moves(piece, tile, colour)
                # check for check
            case _:
                print("FAIL")

    def show_pawn_moves(self, piece: Piece, tile: tuple[str, str], colour: str):
        row, col = tile[0], tile[1]
        piece.is_enpassantable = False
        piece.can_enpassant = False
        if colour == "white":
            if not self.board[row - 1][col]:  # one space forward
                self.possible_moves.append((row - 1, col))
                self.does_move_take.append(False)
                if not piece.has_moved:
                    if row - 2 >= 0:  # check not out of bounds
                        if not self.board[row - 2][col]:  # two spaces forward
                            self.possible_moves.append((row - 2, col))
                            self.does_move_take.append(False)
                            piece.is_enpassantable = True
            if col - 1 >= 0:  # taking piece diagonally left
                if self.board[row - 1][col - 1] is not None:
                    if self.board[row - 1][col - 1].colour == "black":
                        self.possible_moves.append((row - 1, col - 1))
                        self.does_move_take.append(True)
                else:  # en passant check
                    if self.board[row][col - 1] is not None:
                        if (
                            self.board[row][col - 1].colour == "black"
                            and self.board[row][col - 1].type == "pawn"
                        ):
                            if self.board[row][col - 1].is_enpassantable:
                                self.possible_moves.append((row - 1, col - 1))
                                self.does_move_take.append(True)
                                piece.can_enpassant = True

            if col + 1 < 8:  # taking piece diagonally right
                if self.board[row - 1][col + 1] is not None:
                    if self.board[row - 1][col + 1].colour == "black":
                        self.possible_moves.append((row - 1, col + 1))
                        self.does_move_take.append(True)
                else:  # en passant check
                    if self.board[row][col + 1] is not None:
                        if (
                            self.board[row][col + 1].colour == "black"
                            and self.board[row][col + 1].type == "pawn"
                        ):
                            if self.board[row][col + 1].is_enpassantable:
                                self.possible_moves.append((row - 1, col + 1))
                                self.does_move_take.append(True)
                                piece.can_enpassant = True

        else:  # piece is black
            if not self.board[row + 1][col]:  # one space forward
                self.possible_moves.append((row + 1, col))
                self.does_move_take.append(False)
                if not piece.has_moved:
                    if row + 2 < 8:  # check not out of bounds
                        if not self.board[row + 2][col]:  # two spaces forward
                            self.possible_moves.append((row + 2, col))
                            self.does_move_take.append(False)
                            piece.is_enpassantable = True
            if col - 1 >= 0:  # taking piece diagonally left
                if self.board[row + 1][col - 1] is not None:
                    if self.board[row + 1][col - 1].colour == "white":
                        self.possible_moves.append((row + 1, col - 1))
                        self.does_move_take.append(True)
                else:  # en passant check
                    if self.board[row][col - 1] is not None:
                        if (
                            self.board[row][col - 1].colour == "white"
                            and self.board[row][col - 1].type == "pawn"
                        ):
                            if self.board[row][col - 1].is_enpassantable:
                                self.possible_moves.append((row + 1, col - 1))
                                self.does_move_take.append(True)
                                piece.can_enpassant = True

            if col + 1 < 8:  # taking piece diagonally right
                if self.board[row + 1][col + 1] is not None:
                    if self.board[row + 1][col + 1].colour == "white":
                        self.possible_moves.append((row + 1, col + 1))
                        self.does_move_take.append(True)
                else:  # en passant check
                    if self.board[row][col + 1] is not None:
                        if (
                            self.board[row][col + 1].colour == "white"
                            and self.board[row][col + 1].type == "pawn"
                        ):
                            if self.board[row][col + 1].is_enpassantable:
                                self.possible_moves.append((row + 1, col + 1))
                                self.does_move_take.append(True)
                                piece.can_enpassant = True

    def show_rook_moves(self, piece: Piece, tile: tuple[str, str], colour: str):
        row, col = tile[0], tile[1]
        for to_row in range(row + 1, 8):
            if self.board[to_row][col] is not None:
                if self.board[to_row][col].colour != colour:
                    self.possible_moves.append((to_row, col))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((to_row, col))
                self.does_move_take.append(False)

        for to_row in range(row - 1, -1, -1):
            if self.board[to_row][col] is not None:
                if self.board[to_row][col].colour != colour:
                    self.possible_moves.append((to_row, col))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((to_row, col))
                self.does_move_take.append(False)

        for to_col in range(col + 1, 8):
            if self.board[row][to_col] is not None:
                if self.board[row][to_col].colour != colour:
                    self.possible_moves.append((row, to_col))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((row, to_col))
                self.does_move_take.append(False)

        for to_col in range(col - 1, -1, -1):
            if self.board[row][to_col] is not None:
                if self.board[row][to_col].colour != colour:
                    self.possible_moves.append((row, to_col))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((row, to_col))
                self.does_move_take.append(False)

    def show_knight_moves(self, piece: Piece, tile: tuple[str, str], colour: str):
        row, col = tile[0], tile[1]
        if col - 1 >= 0:
            if row - 2 >= 0:  # up left
                if self.board[row - 2][col - 1] is not None:
                    if self.board[row - 2][col - 1].colour != colour:
                        self.possible_moves.append((row - 2, col - 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row - 2, col - 1))
                    self.does_move_take.append(False)
            if row + 2 < 8:  # down left
                if self.board[row + 2][col - 1] is not None:
                    if self.board[row + 2][col - 1].colour != colour:
                        self.possible_moves.append((row + 2, col - 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row + 2, col - 1))
                    self.does_move_take.append(False)

            if col - 2 >= 0:
                if row - 1 >= 0:  # left up
                    if self.board[row - 1][col - 2] is not None:
                        if self.board[row - 1][col - 2].colour != colour:
                            self.possible_moves.append((row - 1, col - 2))
                            self.does_move_take.append(True)
                    else:
                        self.possible_moves.append((row - 1, col - 2))
                        self.does_move_take.append(False)
                if row + 1 < 8:  # left down
                    if self.board[row + 1][col - 2] is not None:
                        if self.board[row + 1][col - 2].colour != colour:
                            self.possible_moves.append((row + 1, col - 2))
                            self.does_move_take.append(True)
                    else:
                        self.possible_moves.append((row + 1, col - 2))
                        self.does_move_take.append(False)

        if col + 1 < 8:
            if row - 2 >= 0:  # up right
                if self.board[row - 2][col + 1] is not None:
                    if self.board[row - 2][col + 1].colour != colour:
                        self.possible_moves.append((row - 2, col + 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row - 2, col + 1))
                    self.does_move_take.append(False)
            if row + 2 < 8:  # down right
                if self.board[row + 2][col + 1] is not None:
                    if self.board[row + 2][col + 1].colour != colour:
                        self.possible_moves.append((row + 2, col + 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row + 2, col + 1))
                    self.does_move_take.append(False)

            if col + 2 < 8:
                if row - 1 >= 0:  # right up
                    if self.board[row - 1][col + 2] is not None:
                        if self.board[row - 1][col + 2].colour != colour:
                            self.possible_moves.append((row - 1, col + 2))
                            self.does_move_take.append(True)
                    else:
                        self.possible_moves.append((row - 1, col + 2))
                        self.does_move_take.append(False)
                if row + 1 < 8:  # right down
                    if self.board[row + 1][col + 2] is not None:
                        if self.board[row + 1][col + 2].colour != colour:
                            self.possible_moves.append((row + 1, col + 2))
                            self.does_move_take.append(True)
                    else:
                        self.possible_moves.append((row + 1, col + 2))
                        self.does_move_take.append(False)

    def show_bishop_moves(self, piece: Piece, tile: tuple[str, str], colour: str):
        row, col = tile[0], tile[1]
        for i in range(1, min(row, col) + 1):  # up left
            if self.board[row - i][col - i] is not None:
                if self.board[row - i][col - i].colour != colour:
                    self.possible_moves.append((row - i, col - i))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((row - i, col - i))
                self.does_move_take.append(False)

        for i in range(1, min(row, 8 - col) + 1):  # up right
            if self.board[row - i][col + i] is not None:
                if self.board[row - i][col + i].colour != colour:
                    self.possible_moves.append((row - i, col + i))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((row - i, col + i))
                self.does_move_take.append(False)

        for i in range(1, min(8 - row, col) + 1):  # down left
            if self.board[row + i][col - i] is not None:
                if self.board[row + i][col - i].colour != colour:
                    self.possible_moves.append((row + i, col - i))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((row + i, col - i))
                self.does_move_take.append(False)

        for i in range(1, min(8 - row, 8 - col) + 1):  # down right
            if self.board[row + i][col + i] is not None:
                if self.board[row + i][col + i].colour != colour:
                    self.possible_moves.append((row + i, col + i))
                    self.does_move_take.append(True)
                break
            else:
                self.possible_moves.append((row + i, col + i))
                self.does_move_take.append(False)

    def show_king_moves(self, piece: Piece, tile: tuple[str, str], colour: str):
        row, col = tile[0], tile[1]
        if col - 1 >= 0:  # left
            if self.board[row][col - 1] is not None:
                if self.board[row][col - 1].colour != colour:
                    self.possible_moves.append((row, col - 1))
                    self.does_move_take.append(True)
            else:
                self.possible_moves.append((row, col - 1))
                self.does_move_take.append(False)
            if row - 1 >= 0:  # up left
                if self.board[row - 1][col - 1] is not None:
                    if self.board[row - 1][col - 1].colour != colour:
                        self.possible_moves.append((row - 1, col - 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row - 1, col - 1))
                    self.does_move_take.append(False)
            if row + 1 < 8:  # down left
                if self.board[row + 1][col - 1] is not None:
                    if self.board[row + 1][col - 1].colour != colour:
                        self.possible_moves.append((row + 1, col - 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row + 1, col - 1))
                    self.does_move_take.append(False)

        if col + 1 < 8:  # right
            if self.board[row][col + 1] is not None:
                if self.board[row][col + 1].colour != colour:
                    self.possible_moves.append((row, col + 1))
                    self.does_move_take.append(True)
            else:
                self.possible_moves.append((row, col + 1))
                self.does_move_take.append(False)
            if row - 1 >= 0:  # up right
                if self.board[row - 1][col + 1] is not None:
                    if self.board[row - 1][col + 1].colour != colour:
                        self.possible_moves.append((row - 1, col + 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row - 1, col + 1))
                    self.does_move_take.append(False)
            if row + 1 < 8:  # down right
                if self.board[row + 1][col + 1] is not None:
                    if self.board[row + 1][col + 1].colour != colour:
                        self.possible_moves.append((row + 1, col + 1))
                        self.does_move_take.append(True)
                else:
                    self.possible_moves.append((row + 1, col + 1))
                    self.does_move_take.append(False)

        if row - 1 >= 0:  # up
            if self.board[row - 1][col] is not None:
                if self.board[row - 1][col].colour != colour:
                    self.possible_moves.append((row - 1, col))
                    self.does_move_take.append(True)
            else:
                self.possible_moves.append((row - 1, col))
                self.does_move_take.append(False)
        if row + 1 < 8:  # down
            if self.board[row + 1][col] is not None:
                if self.board[row + 1][col].colour != colour:
                    self.possible_moves.append((row + 1, col))
                    self.does_move_take.append(True)
            else:
                self.possible_moves.append((row + 1, col))
                self.does_move_take.append(False)
                
        if not piece.has_moved:
            self.can_castle(colour)

    def can_castle(self, colour:str):
        if colour == "white":
            if self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None: # castle left
                if self.board[7][0] is not None:
                    if self.board[7][0].type == "rook":
                        if not self.board[7][0].has_moved:
                            self.possible_moves.append((7, 2))
                            self.does_move_take.append(False)

            if self.board[7][6] is None and self.board[7][5] is None: # castle right
                if self.board[7][7] is not None:
                    if self.board[7][7].type == "rook":
                        if not self.board[7][7].has_moved:
                            self.possible_moves.append((7, 6))
                            self.does_move_take.append(False)
        else: # black
            if self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None: # castle left
                if self.board[0][0] is not None:
                    if self.board[0][0].type == "rook":
                        if not self.board[0][0].has_moved:
                            self.possible_moves.append((0, 2))
                            self.does_move_take.append(False)

            if self.board[0][6] is None and self.board[0][5] is None: # castle right
                if self.board[0][7] is not None:
                    if self.board[0][7].type == "rook":
                        if not self.board[0][7].has_moved:
                            self.possible_moves.append((0, 6))
                            self.does_move_take.append(False)

    def move_piece(self, from_tile, to_tile):
        piece = self.board[from_tile[0]][from_tile[1]]
        if piece.type == "pawn":
            # check for enpassant
            if self.does_move_take[self.possible_moves.index(to_tile)]:
                if self.board[to_tile[0]][to_tile[1]] is None:
                    if piece.colour == "white":
                        self.board[to_tile[0] + 1][to_tile[1]] = None
                    else:
                        self.board[to_tile[0] - 1][to_tile[1]] = None
            
            # check for promotion
            if piece.colour == "white":
                if to_tile[0] == 0:
                    # TODO implement promotion
                    print("-- PROMOTION --")
            else:
                if to_tile[0] == 7:
                    # TODO implement promotion
                    print("-- PROMOTION --")

            piece.has_moved = True

        elif piece.type == "king":
            # check for castling
            if not piece.has_moved:
                if to_tile == (7, 2):
                    self.board[7][3] = self.board[7][0]
                    self.board[7][0] = None
                elif to_tile == (7, 6):
                    self.board[7][5] = self.board[7][7]
                    self.board[7][0] = None
                elif to_tile == (0, 2):
                    self.board[0][3] = self.board[0][0]
                    self.board[0][0] = None
                elif to_tile == (0, 6):
                    self.board[0][5] = self.board[0][7]
                    self.board[0][0] = None

            piece.has_moved = True

        elif piece.type == "rook":
            piece.has_moved = True

        self.board[from_tile[0]][from_tile[1]] = None
        self.board[to_tile[0]][to_tile[1]] = piece

        self.possible_moves = []
        self.does_move_take = []
        self.selected_tile = None
        self.toggle_current_player()

    def check_for_check(self, pos):
        pass

    def check_for_checkmate(self):
        pass

    def click_callback(self, pos):
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE
        tile = (row, col)  # convert to range 0-7 and put in (row, col) format
        if not self.selected_tile:
            if self.board[row][col] is not None:  # if clicked on piece
                piece = self.board[row][col]
                if self.current_player == piece.colour:
                    self.selected_tile = tile
                    self.show_possible_moves(piece, tile)
        else:
            if tile == self.selected_tile:
                self.selected_tile = None
                self.possible_moves = []
            elif tile in self.possible_moves:
                self.move_piece(self.selected_tile, tile)
            else:  # clicked elsewhere
                if self.board[row][col] is not None:  # if clicked on piece
                    piece = self.board[row][col]
                    if self.current_player == piece.colour:
                        self.selected_tile = tile
                        self.show_possible_moves(piece, tile)

    def test(self):
        # # test en passant
        # self.board[6][3] = Piece(
        #     "black", "pawn", "images/black_pawn.png", self.SQUARE_SIZE
        # )
        # self.board[6][3].is_enpassantable = True

        # # test rook
        # self.board[3][0] = Piece(
        #     "white", "rook", "images/white_rook.png", self.SQUARE_SIZE
        # )

        # test knight
        self.board[3][4] = Piece(
            "white", "knight", "images/white_knight.png", self.SQUARE_SIZE
        )

        # # test bishop
        # self.board[3][4] = Piece(
        #     "white", "bishop", "images/white_bishop.png", self.SQUARE_SIZE
        # )

        # # test queen
        # self.board[4][5] = Piece(
        #     "white", "queen", "images/white_queen.png", self.SQUARE_SIZE
        # )

        # # test king
        # self.board[4][6] = Piece(
        #     "white", "king", "images/white_king.png", self.SQUARE_SIZE
        # )

        # # test castling
        # self.board[7][1] = None
        # self.board[7][2] = None
        # self.board[7][3] = None

    def run(self):
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()  # (col, row)
                    self.click_callback(pos)

                # add hover colour

            self.draw_board()

            pygame.display.flip()

            pygame.time.Clock().tick(60)


if __name__ == "__main__":
    import pygame

    game = Game()
