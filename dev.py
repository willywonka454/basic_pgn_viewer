from chess import *
from chessmanager import *
from pgninterpreter import *

game_data = ChessGame()
pgn_data = PGNData("gundersen_h_faul_1928.pgn")
chess_manager = ChessManager(game_data, pgn_data)

print(pgn_data.summary)

def program_loop():
    print("Game:", pgn_data.file)
    user_exit = False
    while user_exit == False:        
        print(chess_manager.curr_state().dev_str())
        
        move_number = pgn_data.data_index
        curr_move = pgn_data.curr_move()                
        prev_move = pgn_data.access_move(move_number - 1)
        next_move = pgn_data.access_move(move_number + 1)
        
        print("Prev move: {}. {}".format(move_number - 1, prev_move['annot']))
        print("Current move: {}. {}".format(move_number, curr_move['annot']))
        print("Next move: {}. {}".format(move_number + 1, next_move['annot']))        
        
        '''print("Move list: ")
        for move in chess_manager.pgn.data:
            print(move['annot'], end = " ")
        '''
        user_exit = user_prompt()

def user_prompt():
    info_text = ""
    info_text += "----------\n" 
    info_text += "n for next move.\n"
    info_text += "p for previous move.\n"
    info_text += "# for a specific move.\n"
    info_text += "e to exit.\n"
    info_text += "----------\n"
    info_text += "User input: "
    
    user_exit = False
    
    user_input = input(info_text)
    
    if user_input == "n": chess_manager.next_state()
    elif user_input == "p": chess_manager.prev_state()
    elif user_input.isdigit(): chess_manager.change_state(int(user_input))
    else: user_exit = True
        
    return user_exit
    
# Start of program.        
program_loop() 