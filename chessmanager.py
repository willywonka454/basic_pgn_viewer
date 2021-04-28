from chess import*
from pgninterpreter import*
    
class ChessManager:
    def __init__(self, game, pgn):
        self.game = game
        self.pgn = pgn
        self.states = []
        self.states_index = 0
        self.create_game_states()
     
    def create_game_states(self):
        currState = self.game.deepcopy()
        
        for move in self.pgn.data:
            currState = currState.deepcopy()
        
            piece = move['piece'] 
        
            protocol = {
                    "start": self.filler_protocol,
                    "pawn": self.universal_protocol,
                    "bishop": self.universal_protocol,
                    "knight": self.universal_protocol,
                    "rook": self.universal_protocol,
                    "queen": self.universal_protocol,
                    "king": self.universal_protocol,
                    "castle": self.castle_protocol
                   }
                  
            protocol[piece](piece, currState, move['color'], move['orig'], move['dest'], move)
            self.states.append(currState)
            self.states_index += 1
            
        self.states_index = 0
        
    def next_state(self):
        if self.states_index >= len(self.states) - 1: self.states_index = self.states_index
        else: self.states_index += 1
        self.game = self.states[self.states_index]
        return self.game
    
    def prev_state(self):
        if self.states_index <= 0: self.states_index = self.states_index
        else: self.states_index -= 1
        self.game = self.states[self.states_index]
        return self.game
    
    def change_state(self, index):
        if index >= len(self.states) - 1: self.states_index = len(self.states) - 1
        elif index <= 0: self.states_index = 0
        else: self.states_index = index
        
        self.game = self.states[self.states_index]
        return self.game
    
    def access_state(self, index):
        if index >= len(self.states) - 1: return self.states[-1]
        elif index <= 0: return self.states[0]
        else: return self.states[index]
    
    def curr_state(self):
        return self.states[self.states_index]
        
    def filler_protocol(self, piece_name, game, color, orig, dest, raw):
        pass
        
    def filler_moves(self, game, piece):
        return []
    
    def castle_protocol(self, piece_name, game, color, orig, dest, raw):
        if orig['rank'] == "KO":
            if color == "white":
                king_orig = { 'rank': 1, 'file': "e" }
                king_dest = { 'rank': 1, 'file': "g" }
                rook_orig = { 'rank': 1, 'file': "h" }
                rook_dest = { 'rank': 1, 'file': "f" }
                self.move_piece(game, king_orig, king_dest, raw)
                self.move_piece(game, rook_orig, rook_dest, raw)
            else:
                king_orig = { 'rank': 8, 'file': "e" }
                king_dest = { 'rank': 8, 'file': "g" }
                rook_orig = { 'rank': 8, 'file': "h" }
                rook_dest = { 'rank': 8, 'file': "f" }
                self.move_piece(game, king_orig, king_dest, raw)
                self.move_piece(game, rook_orig, rook_dest, raw)
        else:
            if color == "white":
                king_orig = { 'rank': 1, 'file': "e" }
                king_dest = { 'rank': 1, 'file': "c" }
                rook_orig = { 'rank': 1, 'file': "a" }
                rook_dest = { 'rank': 1, 'file': "d" }
                self.move_piece(game, king_orig, king_dest, raw)
                self.move_piece(game, rook_orig, rook_dest, raw)
            else:
                king_orig = { 'rank': 8, 'file': "e" }
                king_dest = { 'rank': 8, 'file': "c" }
                rook_orig = { 'rank': 8, 'file': "a" }
                rook_dest = { 'rank': 8, 'file': "d" }
                self.move_piece(game, king_orig, king_dest)
                self.move_piece(game, rook_orig, rook_dest)
    
    def universal_protocol(self, piece_name, game, color, orig, dest, raw):
        piece = self.find_piece(piece_name, game, color, orig, dest)
    
        if piece:
            piece_orig = { 'rank': piece.rank, 'file': piece.file }
            self.move_piece(game, piece_orig, dest, raw)
        
    def find_piece(self, piece_name, game, color, orig, dest):
        for rank in ranks.keys():
            for file in files.keys():
                piece = game.piece_at(file, rank)
                if piece and piece.name == piece_name and piece.color == color:                                    
                    return_moves = {
                                    "pawn": self.return_pawn_moves,
                                    "bishop": self.return_bishop_moves,
                                    "knight": self.return_knight_moves,
                                    "rook": self.return_rook_moves,
                                    "queen": self.return_queen_moves,
                                    "king": self.return_king_moves,
                                }                    
                    valid_moves = return_moves[piece.name](game, piece)                    
                    correct_move = self.check_moves(valid_moves, dest)                    
                    correct_orig = self.check_orig(piece, orig)                    
                    if correct_move and correct_orig:                         
                        return piece
        return None
    
    def check_orig(self, piece, orig):
        matches_required = 0
        
        if orig['rank']:
            matches_required += 1
            if piece.rank == int(orig['rank']): matches_required -= 1
        if orig['file']:
            matches_required += 1
            if piece.file == orig['file']: matches_required -=1
        
        if matches_required == 0: return True
        return False
    
    def check_moves(self, valid_moves, dest):
        for move in valid_moves:
            if move['rank'] == int(dest['rank']) and move['file'] == dest['file']:
                return True
        return False
    
    def move_piece(self, game, orig, dest, raw):
        target_file = dest['file']
        target_rank = int(dest['rank'])
        
        orig_file = orig['file']
        orig_rank = int(orig['rank'])
    
        piece = game.piece_at(orig_file, orig_rank)
        piece.file = target_file
        piece.rank = target_rank
        
        promotion_dict = {
                            "queen": Queen(),
                            "rook": Rook(),
                            "knight": Knight(),
                            "bishop": Bishop()
                        }
        
        if piece.name == "pawn" and (piece.rank == 8 or piece.rank == 1):
            promotion_type = promotion_dict[raw['promotion']]
            piece = promotion_type.deepcopy(piece.color, piece.rank, piece.file)        
    
        game.set_square(orig_file, orig_rank, None)
        game.set_square(target_file, target_rank, piece)
        
        if piece.name == "pawn":
            piece.moved = True
        if piece.name == "king":
            piece.moved = True
        
    
    def default_cycle(self, game, piece_to_move, rank_modif, file_modif, rank_limit_upper, 
                        rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves):
        rev = list(files.keys())
    
        rank = piece_to_move.rank
        file = piece_to_move.file
        
        def limit_obeyed(modif, upper_limit, lower_limit, val):
            if (val <= lower_limit and modif < 0): return False
            elif (val >= upper_limit and modif > 0): return False
            else: return True
        
        rank_limit_obeyed = limit_obeyed(rank_modif, rank_limit_upper, rank_limit_lower, rank)
        file_limit_obeyed = limit_obeyed(file_modif, file_limit_upper, file_limit_lower, convert_file_to_num(file))
        while rank_limit_obeyed and file_limit_obeyed:
            rank = rank + rank_modif
            file = file_add(file, file_modif)
            new_move = { 'rank': rank, 'file': file }
        
            obstruction_piece = game.piece_at(file, rank)
            if obstruction_piece: 
                if obstruction_piece.color == piece_to_move.color: break
                else:
                    valid_moves.append(new_move)
                    break
            
            valid_moves.append(new_move)
            
            rank_limit_obeyed = limit_obeyed(rank_modif, rank_limit_upper, rank_limit_lower, rank)
            file_limit_obeyed = limit_obeyed(file_modif, file_limit_upper, file_limit_lower, convert_file_to_num(file))
    
    def return_king_moves(self, game, king):
        valid_moves = []
                
        rank_limit_upper = king.rank + 1
        if king.rank + 1 > 8: rank_limit_upper = 8
        
        rank_limit_lower = king.rank - 1
        if king.rank - 1 < 1: rank_limit_lower = 1
        
        file_limit_upper = files[king.file] + 1 + 1
        if files[king.file] + 1 + 1 > 8: file_limit_upper = 8 
        
        file_limit_lower = files[king.file] + 1 - 1
        if files[king.file] + 1 - 1 < 1: rank_limit = 1
        
        straight_moves = self.return_rook_moves(game, king, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower)
        diagonal_moves = self.return_bishop_moves(game, king, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower)        
        
        valid_moves = straight_moves + diagonal_moves                   
        
        return valid_moves
    
    def return_queen_moves(self, game, queen):
        valid_moves = []
    
        straight_moves = self.return_rook_moves(game, queen)
        diagonal_moves = self.return_bishop_moves(game, queen)
        
        valid_moves = straight_moves + diagonal_moves
        
        return valid_moves
    
    def return_rook_moves(self, game, rook, rank_limit_upper = 8, rank_limit_lower = 1, file_limit_upper = 8, file_limit_lower = 1):
        valid_moves = []
        
        rank_modif = 1
        file_modif = 0
        self.default_cycle(game, rook, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        rank_modif = -1
        file_modif = 0
        self.default_cycle(game, rook, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        rank_modif = 0
        file_modif = 1
        self.default_cycle(game, rook, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        rank_modif = 0
        file_modif = -1
        self.default_cycle(game, rook, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        return valid_moves
    
    def return_knight_moves(self, game, knight):
        '''
        
          -21012+
         2 #X#X#
         1 X###X
         0 ##K##
        -1 X###X
        -2 #X#X#
        
          (x , y)
        [ (-2, 1), (-2, -1), (2, 1), (2, -1) ],
        [ (-1, 2), (-1, -2), (1, 2), (1, -2) ]
        
        '''
    
        valid_moves = []
        
        # a: 0, b: 1, c: 2 ... h: 7
        rev = list(files.keys())
        
        rank_modif = [-2, -1, 1, 2]
        file_modif = [-2, -1, 1, 2]
        
        if(knight.rank < 3): rank_modif.remove(-2)
        if(knight.rank < 2): rank_modif.remove(-1)
        if(knight.rank > 6): rank_modif.remove(2)
        if(knight.rank > 7): rank_modif.remove(1)
        
        knight_num_file = files[knight.file] + 1
        if(knight_num_file < 3): file_modif.remove(-2)
        if(knight_num_file < 2): file_modif.remove(-1)
        if(knight_num_file > 6): file_modif.remove(2)
        if(knight_num_file > 7): file_modif.remove(1)
        
        for rm in rank_modif:
            for fm in file_modif:
                if abs(rm) == abs(fm): continue 
            
                new_rank = knight.rank + rm
                new_file = rev[knight_num_file - 1 + fm]
                
                piece = game.board[ (ranks[new_rank]) ][ (files[new_file]) ]
                if piece and piece.color == knight.color: continue
                
                new_move = { 'rank': new_rank, 'file': new_file }
                valid_moves.append(new_move)
        
        return valid_moves
            
    def return_bishop_moves(self, game, bishop, rank_limit_upper = 8, rank_limit_lower = 1, file_limit_upper = 8, file_limit_lower = 1):
        valid_moves = []
        
        rank_modif = 1
        file_modif = 1
        self.default_cycle(game, bishop, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        rank_modif = 1
        file_modif = -1
        self.default_cycle(game, bishop, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        rank_modif = -1
        file_modif = 1
        self.default_cycle(game, bishop, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        rank_modif = -1
        file_modif = -1
        self.default_cycle(game, bishop, rank_modif, file_modif, rank_limit_upper, rank_limit_lower, file_limit_upper, file_limit_lower, valid_moves)
        
        return valid_moves
        
    def return_pawn_moves(self, game, pawn):
        valid_moves = []
        
        rank_modif = 1
        if pawn.color == "white": rank_modif = 1
        if pawn.color == "black": rank_modif = -1
        
        if (pawn.rank <= 7 and pawn.color == "white") or (pawn.rank >= 2 and pawn.color == "black"):
            new_rank = pawn.rank + rank_modif
            new_file = files[pawn.file]
            piece = game.board[ranks[new_rank]][new_file]
            if not piece:
                new_move = { 'rank': new_rank, 'file': pawn.file }
                valid_moves.append(new_move)
                if pawn.moved == False:
                    new_rank = pawn.rank + (rank_modif * 2)
                    new_file = files[pawn.file]
                    piece = game.board[ranks[new_rank]][new_file]
                    if not piece:
                        new_move = { 'rank': new_rank, 'file': pawn.file }
                        valid_moves.append(new_move)
                
        rev = list(files.keys())
        pawn_num_file = files[pawn.file]
        file_modif = [1, -1]
        
        if (pawn.rank <= 7 and pawn.color == "white") or (pawn.rank >= 2 and pawn.color == "black"):
            if pawn_num_file <= 0: file_modif.remove(-1)
            if pawn_num_file >= 7: file_modif.remove(1)
            for fm in file_modif:
                new_rank = pawn.rank + rank_modif
                new_file = rev[pawn_num_file + fm]
                
                piece = game.board[ (ranks[new_rank]) ][ (files[new_file]) ]
                if not piece:
                    if not self.en_passant(game, new_rank, new_file, pawn): continue
                if piece and piece.color == pawn.color: continue
                
                new_move = { 'rank': new_rank, 'file': new_file }
                valid_moves.append(new_move)
            
        return valid_moves
        
    def en_passant(self, curr_state, target_rank, target_file, pawn):
        one_states_ago = self.access_state(self.states_index - 1)
        two_states_ago = self.access_state(self.states_index - 2)
        
        if pawn.color == "white":
            if pawn.rank != 5 and target_rank != 6: return False
            if not two_states_ago.board[ ranks[7] ][ (files[target_file]) ]: return False
            if one_states_ago.board[ ranks[7] ][ (files[target_file]) ]: return False
            if not curr_state.board[ ranks[5] ][ (files[target_file]) ]: return False
            curr_state.board[ ranks[5] ][ (files[target_file]) ] = None
        else:
            if pawn.rank != 4 and target_rank != 3: return False
            if not two_states_ago.board[ ranks[2] ][ (files[target_file]) ]: return False
            if one_states_ago.board[ ranks[2] ][ (files[target_file]) ]: return False
            if not curr_state.board[ ranks[4] ][ (files[target_file]) ]: return False
            curr_state.board[ ranks[4] ][ (files[target_file]) ] = None
            
        return True