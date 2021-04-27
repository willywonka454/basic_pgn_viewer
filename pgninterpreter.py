class PGNData:
    def __init__(self, file = "examplegame.pgn"):
        self.summary = ""
        self.moves = []
        self.file = file
        self.extract_data()
        self.data = self.decode_moves()
        self.data_index = 0

    def next_move(self):
        if self.data_index < len(self.data) - 1:
            self.data_index += 1        
            return self.data[self.data_index]
        return self.data[self.data_index]
    
    def prev_move(self):
        if self.data_index > 0:
            self.data_index -= 1        
            return self.data[self.data_index]
        return self.data[self.data_index]
        
    def curr_move(self):
        return self.data[self.data_index]
        
    def change_move(self, index):
        if index >= len(self.data) - 1: 
            self.data_index = len(self.data) - 1            
        elif index <= 0: 
            self.data_index = 0
        else:
            self.data_index = index
            
        return self.data[self.data_index]
        
    def access_move(self, index):
        if index >= len(self.data) - 1: return self.data[-1]
        elif index < 0: return self.data[0]
        else: return self.data[index]
        
    def extract_data(self):
        f = open(self.file, "r")
        raw_contents = f.read()
        split_contents = raw_contents.split()
    
        i = 0
        while i < len(split_contents):
            if split_contents[i] == "1.":
                break
            i += 1
        while i < len(split_contents) - 2:            
            white_turn = split_contents[i + 1]
            black_turn = split_contents[i + 2]
            move = []            
            move.append(white_turn)
            if black_turn != "1-0" and black_turn != "0-1" and black_turn != "1/2-1/2":
                move.append(black_turn)                
            self.moves.append(move)
            i += 3
            
    def decode_moves(self):
        data = []
        
        start_cell = { "annot": "start", "color": "start", "piece": "start", "action": "start", "dest": "start", "orig": "start" }
        data.append(start_cell)              
        
        for move in self.moves:
            for idx, turn in enumerate(move):
                color = "white"
                if idx > 0: color = "black"
                
                action = self.detect_action(turn)
                piece = self.detect_piece(turn[0])
                origin = self.detect_origin(action, piece, turn)
                dest = self.detect_dest(turn)
                
                dest_str = "destination: {}{}".format(dest["file"], dest["rank"])
                piece_str = "piece: {}".format(piece)
                action_str = "action: {}".format(action)
                origin_str = "origin: {}{}".format(origin["file"], origin["rank"])
                self.summary += ("{:6s} {:6s} {:20s} {:20s} {:20s} {:15s}\n".format(turn, color, dest_str, piece_str, action_str, origin_str))
                
                data_cell = {   
                                "annot": turn,
                                "color": color, 
                                "piece": piece, 
                                "action": action, 
                                "dest": dest, 
                                "orig": origin    
                            }
                
                if piece == "pawn" and dest["rank"] == '8':
                    data_cell['promotion'] = self.detect_promot(turn)
                    
                data.append(data_cell)
        return data
    
    def __str__(self):
        return self.summary
    
    def detect_dest(self, input):
        start = len(input) - 2
        end = len(input)
        if "O-O-O" in input: return {"rank": "QO", "file": "QO"}
        if "O-O" in input: return {"rank": "KO", "file": "KO"}
        if ("+" in input) or ("#" in input): 
            start -= 1
            end -= 1
        if "=" in input:
            start -= 2
            end -= 2
        if start >= end: return {"rank": "ERR", "file": "ERR"}
        file = input[start]
        rank = input[end - 1]
        retVal = {"rank": rank, "file": file}
        return retVal
    
    def detect_origin(self, action, piece, input):
        start = 1
        end = len(input)
        if "O-O-O" in input: return {"rank": "QO", "file": "QO"}
        if "O-O" in input: return {"rank": "KO", "file": "KO"}
        if piece == "pawn": start = 0
        if ("+" in input) or ("#" in input): end -= 1
        if "=" in input: end -= 1
        if action == "captures":
            end = input.index("x")
        if action == "moves":
            end -= 2
        if start >= end: return {"rank": None, "file": None}
        if len(input[start:end]) == 1: 
            if input[start:end].isdigit(): return {"rank": input[start:end], "file": None}
            return {"rank": None, "file": input[start:end]}
        return input[start:end]            
    
    def detect_action(self, input):
        if "x" in input: return "captures"
        return "moves"
    
    def detect_promot(self, input):
        target = len(input) - 1
        if "+" in input: target -= 1
        if "#" in input: target -= 1
        piece_letter = input[target]
        return self.detect_piece(piece_letter)
    
    def detect_piece(self, input):
        pieces = {
                    "B": "bishop",
                    "N": "knight",
                    "R": "rook",
                    "Q": "queen",
                    "K": "king",
                    "O": "castle"
                }                
        if input.islower(): return "pawn"
        return pieces[input]