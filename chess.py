ranks = { 
           1: 0, 
           2: 1, 
           3: 2, 
           4: 3,
           5: 4,
           6: 5,
           7: 6,
           8: 7
        }
        
files = { 
          "a": 0, 
          "b": 1, 
          "c": 2, 
          "d": 3,
          "e": 4,
          "f": 5,
          "g": 6,
          "h": 7
        }

class Piece:
    name = "generic piece"
    symbol = "generic symbol"
    
    def __init__(self, color = "white", rank = 1, file = "a"):
        self.color = color
        self.rank = rank
        self.file = file
    
    def deepcopy(self, color = None, rank = None, file = None):
        if color == None: color = self.color
        if rank == None: rank = self.rank
        if file == None: file = self.file
    
        obj_type = type(self)
        copy = obj_type(color, rank, file)
        return copy
    
    def __repr__(self):
        return "{} {} {}{}".format(self.color, self.name, self.file, self.rank)
        
    def __str__(self):
        return "{} {}".format(self.color, self.name)
        
class King(Piece):
    name = "king"
    symbol = "K"
    
    def __init__(self, color = "white", rank = 1, file = "a", moved = False):
        self.moved = moved
        super().__init__(color, rank, file)
        
    def deepcopy(self):
        copy = super().deepcopy()
        copy.moved = self.moved
        return copy
        
class Queen(Piece):
    name = "queen"
    symbol = "Q"
    
    def __init__(self, color = "white", rank = 1, file = "a"):
        super().__init__(color, rank, file)
        
class Rook(Piece):
    name = "rook"
    symbol = "R"
    
    def __init__(self, color = "white", rank = 1, file = "a"):
        super().__init__(color, rank, file)
        
class Bishop(Piece):
    name = "bishop"
    symbol = "B"
    
    def __init__(self, color = "white", rank = 1, file = "a"):
        super().__init__(color, rank, file)
        
class Knight(Piece):
    name = "knight"
    symbol = "N"
    
    def __init__(self, color = "white", rank = 1, file = "a"):
        super().__init__(color, rank, file)
        
class Pawn(Piece):
    name = "pawn"
    symbol = ""
    
    def __init__(self, color = "white", rank = 1, file = "a", moved = False):
        self.moved = moved
        super().__init__(color, rank, file)
    
    def deepcopy(self):
        copy = super().deepcopy()
        copy.moved = self.moved
        return copy
    
class ChessGame:
    def __init__(self):                
        self.board = [  [Rook("white", 1, "a"), Knight("white", 1, "b"), Bishop("white", 1, "c"), Queen("white", 1, "d"), King("white", 1, "e"), Bishop("white", 1, "f"), Knight("white", 1, "g"), Rook("white", 1, "h")],
                        [Pawn("white", 2, "a"), Pawn("white", 2, "b"), Pawn("white", 2, "c"), Pawn("white", 2, "d"), Pawn("white", 2, "e"), Pawn("white", 2, "f"), Pawn("white", 2, "g"), Pawn("white", 2, "h")],
                        [None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None],
                        [Pawn("black", 7, "a"), Pawn("black", 7, "b"), Pawn("black", 7, "c"), Pawn("black", 7, "d"), Pawn("black", 7, "e"), Pawn("black", 7, "f"), Pawn("black", 7, "g"), Pawn("black", 7, "h")],
                        [Rook("black", 8, "a"), Knight("black", 8, "b"), Bishop("black", 8, "c"), Queen("black", 8, "d"), King("black", 8, "e"), Bishop("black", 8, "f"), Knight("black", 8, "g"), Rook("black", 8, "h")], ]                 
    
    def deepcopy(self):
        copy = ChessGame()
        for rank in range(8):
            for file in range(8):
                target_piece = self.board[rank][file]
                if target_piece: copy.board[rank][file] = target_piece.deepcopy()
                else: copy.board[rank][file] = None
        return copy

    def dev_str(self):
        retval = ""
        for rank in reversed(range(8)):
            retval += str(rank + 1); retval += " "*2
            for file in range(8):
                piece = self.board[rank][file]
                if piece: 
                    retval += "{}{:1}{}{}".format(piece.color[0].upper(), piece.symbol, piece.file, piece.rank)
                    retval += " "*5
                else: 
                    retval += "XX  "
                    retval += " "*5
            retval += "\n"
        retval += "   {:9}{:9}{:9}{:9}{:9}{:9}{:9}{:9}".format("a", "b", "c", "d", "e", "f", "g", "h")
        return retval