class Piece:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position
        self.value = self.set_value()
    def set_value(self):
        if self.name == 'King':
            return 1000  # Highest value
        elif self.name == 'Rook':
            return 50  
        elif self.name == 'Knight' or self.name == 'Bishop':
            return 30  # Third highest value
        elif self.name == 'Squire' or self.name == 'Combatant':
            return 20  # Lowest valuee
    def update_pos(self, new_pos):
    # Create a new instance of the current class with updated position
        return self.__class__(self.color, new_pos)
    def __repr__(self):
        return f"{self.name}, {self.color}, {self.position}"
        
class King(Piece):
    def __init__(self, color, position):
        super().__init__("King", color, position)
    def legal_moves(self, m_coords, b_coords):
        legal_moves = []
        row, col = self.position
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:  # Exclude the current position
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if (new_row, new_col) not in m_coords:
                            legal_moves.append(((row, col), (new_row, new_col)))
        return legal_moves
class Rook(Piece):
    def __init__(self, color, position):
        super().__init__("Rook", color, position)
    def legal_moves(self, m_coords, o_coords):
        legal_moves = []
        row, col = self.position
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if (new_row, new_col) in m_coords:
                        break
                    elif (new_row, new_col) in o_coords:
                        legal_moves.append(((row, col), (new_row, new_col)))
                        break
                    else:
                        legal_moves.append(((row, col), (new_row, new_col)))
                else:
                    break
        return legal_moves
class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__("Bishop", color, position)
    def legal_moves(self, m_coords, o_coords):
        legal_moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    # Check if the new position is empty
                    if (new_row, new_col) not in m_coords and (new_row, new_col) not in o_coords:
                        legal_moves.append(((row, col), (new_row, new_col)))
                    # Check if the new position has an opponent's piece
                    elif (new_row, new_col) in o_coords:
                        legal_moves.append(((row, col), (new_row, new_col)))
                        break
                    else:
                        break  # Stop if there's own piece in the way
                else:
                    break  # Stop if out of board bounds
        return legal_moves
class Knight(Piece):
    def __init__(self, color, position):
        super().__init__("Knight", color, position)
    def legal_moves(self, m_coords, b_coords):
        legal_moves = []
        row, col = self.position
        
        # Define all possible knight move offsets
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the new position is empty or has an opponent's piece
                if (new_row, new_col) not in m_coords:
                    legal_moves.append(((row, col), (new_row, new_col)))
        
        return legal_moves
class Squire(Piece):
    def __init__(self, color, position):
        super().__init__("Squire", color, position)
    def legal_moves(self, m_coords, b_coords):
        legal_moves = []
        row, col = self.position
        
        # Define all possible offsets for Manhattan distance of 2
        squire_moves = [(-2, 0), (-1, 1), (0, 2), (1, 1), (2, 0), (1, -1), (0, -2), (-1, -1)]
        
        for dr, dc in squire_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the new position is empty or has an opponent's piece
                if (new_row, new_col) not in m_coords:
                    legal_moves.append(((row, col), (new_row, new_col)))
        
        return legal_moves
class Combatant(Piece):
    def __init__(self, color, position):
        super().__init__("Combatant", color, position)
    def legal_moves(self, m_coords, o_coords):
        legal_moves = []
        row, col = self.position
        
        # Define all possible offsets for non-capturing moves (orthogonal)
        non_capturing_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Define all possible offsets for capturing moves (diagonal)
        capturing_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in non_capturing_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the new position is empty or has an opponent's piece
                if (new_row, new_col) not in m_coords and (new_row, new_col) not in o_coords:
                    legal_moves.append(((row, col), (new_row, new_col)))
        
        for dr, dc in capturing_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the new position has an opponent's piece
                if (new_row, new_col) in o_coords:
                    legal_moves.append(((row, col), (new_row, new_col)))
        
        return legal_moves
def create_state(pieces, color):
    m_coords = set()
    o_coords = set()
    m_pieces = []
    o_pieces = []
    check = []
    capture = []
    nochange = []
    total = []
    for x in pieces:
        if x.color == color:
            m_coords.add(x.position)
            m_pieces.append(x)
        else:
            o_coords.add(x.position)
            o_pieces.append(x)
    for p in m_pieces:
        moves = p.legal_moves(m_coords, o_coords)
        for x, y in moves:
            if y in o_coords:
                flag = False
                new_o = []
                for z in o_pieces:
                    if z.position == y:
                        if z.name == "King":
                            flag = True
                    else:
                        new_o.append(z)
                new_m = [z for z in m_pieces if z.position != p.position]
                up_p = p.update_pos(y)
                new_m.append(up_p)
                new_s = new_m + new_o
                if flag == True:
                    check.append([(x,y),new_s, flag])
                else:
                    capture.append([(x,y),new_s, flag])
            else:
                new_m = [z for z in m_pieces if z.position != p.position]
                up_p = p.update_pos(y)
                new_m.append(up_p)
                new_o = o_pieces.copy()
                new_s = new_m + new_o
                nochange.append([(x,y),new_s, False])
    total = check + capture + nochange
    return total
                   
def studentAgent(gameboard):
    best_move = None
    pieces = setUpBoard(gameboard)
    pos_states = create_state(pieces, "white") 
    best_eval = float('-inf')
    for state in pos_states:
        #if state is not created then create the state 
        #copy the state and make move
        move, a_state, flag = state
        eval = alpha_beta(a_state, 4, float('-inf'), float('inf'), "black", flag) #might need to add changes here 
        #print(move, eval, best_eval)
        if eval > best_eval:  #i think its only >
            best_eval = eval
            best_move = move
    #unapply board move
    return best_move  
def get_legal_moves(gameboard, color):
    legal_moves = []
    pieces = setUpBoard(gameboard)
    black_coords = set()
    white_pieces = []
    white_coords = set()
    for x in pieces:
        if x.color == 'white':
            white_pieces.append(x)
            white_coords.add(x.position)
        else:
            black_coords.add(x.position)
    for x in white_pieces:
        legal_moves.extend(x.legal_moves(white_coords, black_coords))
    return legal_moves
def evaluate(board):
    m_piece = list(filter(lambda x: x.color == "white", board))
    o_piece = list(filter(lambda x: x.color != "white", board))
    return sum(map(lambda x: x.value, m_piece)) - sum(map(lambda x: x.value, o_piece))
count_val = 0
count_e = 0
def alpha_beta(board, depth, alpha, beta, color, flag):
    global count_val
    global count_e
    if depth == 0 or flag:
        count_e +=1
        return evaluate(board)    
    legal_moves = create_state(board, color)
    # order moves so the ones which capture or kill gets executed first
    if color == "white":
        max_eval = float('-inf')
        #order the legal moves based on check then capture 
        for move in legal_moves:
            #ok instead of copying use the dictionary d[hash] = piece there if any 
            #make the move so like 
            eval = alpha_beta(move[1], depth - 1, alpha, beta, "black", move[2])
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            #unapply move here: if got no d[hash] then make the curr None then 
            if beta <= alpha:
                
                count_val += 1
                break
        return max_eval
    else:
        
        min_eval = float('inf')
        for move in legal_moves:
            eval = alpha_beta(move[1], depth - 1, alpha, beta, "white", move[2])
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                count_val +=1
                break
        return min_eval
# get the board and the pieces 
def setUpBoard(gameboard):
    pieces = []
    for piece in gameboard:
        name, color, pos = piece
        if name == "Rook":
            new_p = Rook(color, pos)
            pieces.append(new_p)
        elif name == "Knight":
            new_p = Knight(color, pos)
            pieces.append(new_p)
        elif name == "Combatant":
            new_p = Combatant(color, pos)
            pieces.append(new_p)
        elif name == "Bishop":
            new_p = Bishop(color, pos)
            pieces.append(new_p)
        elif name == "Bishop":
            new_p = Bishop(color, pos)
            pieces.append(new_p)
        elif name == "Squire":
            new_p = Squire(color, pos)
            pieces.append(new_p)
        elif name == "King":
            new_p = King(color, pos)
            pieces.append(new_p)
    return pieces




b1 = [('Rook', 'white', (5, 1)), 
        ('Rook', 'black', (1, 0)), 
        ('Knight', 'white', (4, 6)), 
        ('Knight', 'black', (5, 4)), 
        ('Knight', 'white', (0, 5)), 
        ('Knight', 'black', (2, 0)), 
        ('Combatant', 'white', (4, 0)), 
        ('Combatant', 'black', (5, 0)), 
        ('Combatant', 'white', (5, 3)), 
        ('Combatant', 'black', (5, 6)), 
        ('Combatant', 'white', (7, 1)), 
        ('Combatant', 'black', (0, 1)), 
        ('Combatant', 'white', (0, 4)), 
        ('Combatant', 'black', (7, 5)), 
        ('Bishop', 'white', (3, 4)), 
        ('Bishop', 'white', (1, 1)), 
        ('Bishop', 'black', (6, 1)), 
        ('Bishop', 'black', (4, 2)), 
        ('King', 'black', (0, 6)), 
        ('King', 'white', (7, 7))]
'''
get_legal_moves(b1, 'white') = [((7, 7), (6, 6)), ((0, 5), (1, 3)), ((3, 4), (5, 6)), ((1, 1), (2, 0)), ((7, 1), (7, 2)), ((1, 1), (4, 4)), ((5, 1), (5, 0)), ((5, 3), (6, 3)), ((4, 0), (3, 0)), ((5, 1), (6, 1)), ((1, 1), (0, 0)), ((3, 4), (4, 5)), ((3, 4), (1, 2)), ((4, 6), (6, 5)), ((4, 6), (2, 5)), ((3, 4), (2, 3)), ((1, 1), (3, 3)), ((5, 1), (5, 2)), ((3, 4), (2, 5)), ((3, 4), (4, 3)), ((0, 5), (2, 6)), ((3, 4), (6, 1)), ((1, 1), (6, 6)), ((4, 6), (2, 7)), ((0, 4), (1, 4)), ((1, 1), (5, 5)), ((7, 7), (6, 7)), ((3, 4), (0, 1)), ((5, 3), (4, 3)), ((4, 6), (6, 7)), ((7, 7), (7, 6)), ((3, 4), (0, 7)), ((0, 5), (1, 7)), ((5, 1), (2, 1)), ((4, 0), (4, 1)), ((1, 1), (0, 2)), ((5, 3), (5, 2)), ((3, 4), (1, 6)), ((5, 3), (4, 2)), ((4, 6), (5, 4)), ((1, 1), (2, 2)), ((5, 1), (4, 1)), ((0, 5), (2, 4)), ((0, 4), (0, 3)), ((5, 1), (3, 1)), ((7, 1), (7, 0)), ((3, 4), (5, 2))]
'''

b2 = [('Rook', 'white', (6, 3)), 
      ('Rook', 'black', (0, 1)), 
      ('Knight', 'white', (2, 4)), 
      ('Knight', 'black', (3, 1)), 
      ('Knight', 'white', (5, 6)), 
      ('Knight', 'black', (5, 7)), 
      ('Combatant', 'white', (7, 5)), 
      ('Combatant', 'black', (3, 5)), 
      ('Combatant', 'white', (2, 2)), 
      ('Combatant', 'black', (6, 6)), 
      ('Bishop', 'white', (4, 2)), 
      ('Bishop', 'white', (5, 4)), 
      ('Bishop', 'black', (0, 3)), 
      ('Bishop', 'black', (1, 7)), 
      ('Squire', 'white', (1, 6)), 
      ('Squire', 'white', (1, 3)), 
      ('Squire', 'black', (7, 7)), 
      ('Squire', 'black', (0, 7)), 
      ('King', 'black', (0, 0)), 
      ('King', 'white', (7, 4))]
'''
get_legal_moves(b2, 'white') = [((2, 4), (4, 5)), ((6, 3), (6, 2)), ((4, 2), (3, 3)), ((2, 4), (0, 3)), ((1, 3), (1, 1)), ((5, 6), (3, 7)), ((2, 2), (1, 2)), ((7, 5), (6, 6)), ((1, 3), (1, 5)), ((5, 4), (7, 6)), ((4, 2), (3, 1)), ((1, 3), (0, 4)), ((6, 3), (2, 3)), ((6, 3), (6, 5)), ((7, 4), (6, 5)), ((2, 4), (1, 2)), ((7, 5), (6, 5)), ((4, 2), (5, 1)), ((6, 3), (4, 3)), ((1, 6), (0, 7)), ((5, 4), (2, 1)), ((5, 4), (3, 2)), ((1, 6), (2, 7)), ((2, 4), (0, 5)), ((5, 4), (4, 5)), ((5, 4), (4, 3)), ((6, 3), (6, 6)), ((1, 3), (3, 3)), ((1, 3), (0, 2)), ((1, 6), (0, 5)), ((4, 2), (6, 0)), ((1, 6), (2, 5)), ((6, 3), (6, 0)), ((5, 6), (3, 5)), ((5, 6), (4, 4)), ((5, 4), (6, 5)), ((2, 2), (2, 1)), ((6, 3), (3, 3)), ((6, 3), (5, 3)), ((2, 2), (2, 3)), ((2, 2), (3, 1)), ((2, 4), (3, 2)), ((6, 3), (7, 3)), ((4, 2), (5, 3)), ((2, 4), (4, 3)), ((5, 4), (2, 7)), ((2, 2), (3, 2)), ((4, 2), (6, 4)), ((6, 3), (6, 4)), ((2, 4), (3, 6)), ((5, 4), (3, 6)), ((6, 3), (6, 1)), ((7, 4), (7, 3)), ((1, 6), (3, 6)), ((7, 5), (7, 6)), ((7, 4), (6, 4)), ((5, 6), (7, 7)), ((1, 6), (1, 4)), ((5, 6), (6, 4)), ((5, 4), (1, 0))]
'''

b3 = [('Rook', 'white', (6, 7)), 
      ('Rook', 'black', (7, 6)), 
      ('Combatant', 'white', (5, 6)), 
      ('Combatant', 'black', (3, 5)), 
      ('Combatant', 'white', (7, 2)), 
      ('Combatant', 'black', (2, 2)), 
      ('Combatant', 'white', (1, 7)), 
      ('Combatant', 'black', (7, 7)), 
      ('Combatant', 'white', (2, 1)), 
      ('Combatant', 'black', (4, 5)), 
      ('Bishop', 'white', (0, 3)), 
      ('Bishop', 'white', (3, 3)), 
      ('Bishop', 'black', (0, 6)), 
      ('Bishop', 'black', (6, 1)), 
      ('Squire', 'white', (3, 6)), 
      ('Squire', 'black', (4, 3)), 
      ('King', 'black', (0, 0)), 
      ('King', 'white', (7, 1))]
'''
get_legal_moves(b3, 'white') = [((3, 6), (4, 7)), ((3, 6), (2, 7)), ((6, 7), (6, 3)), ((1, 7), (1, 6)), ((3, 6), (2, 5)), ((0, 3), (1, 2)), ((7, 2), (7, 3)), ((5, 6), (5, 5)), ((3, 3), (2, 4)), ((7, 2), (6, 1)), ((6, 7), (5, 7)), ((3, 3), (4, 2)), ((6, 7), (6, 4)), ((3, 6), (4, 5)), ((3, 3), (6, 0)), ((3, 3), (2, 2)), ((5, 6), (4, 5)), ((6, 7), (6, 6)), ((6, 7), (2, 7)), ((3, 6), (3, 4)), ((6, 7), (6, 1)), ((2, 1), (3, 1)), ((5, 6), (5, 7)), ((3, 3), (7, 7)), ((3, 3), (0, 6)), ((5, 6), (6, 6)), ((7, 1), (6, 0)), ((7, 1), (7, 0)), ((6, 7), (6, 5)), ((3, 3), (6, 6)), ((3, 3), (1, 5)), ((1, 7), (0, 7)), ((7, 1), (6, 2)), ((1, 7), (0, 6)), ((0, 3), (2, 5)), ((2, 1), (1, 1)), ((3, 6), (1, 6)), ((6, 7), (6, 2)), ((5, 6), (4, 6)), ((0, 3), (1, 4)), ((3, 3), (5, 5)), ((3, 3), (4, 4)), ((1, 7), (2, 7)), ((2, 1), (2, 0)), ((3, 3), (5, 1)), ((6, 7), (7, 7)), ((6, 7), (4, 7)), ((7, 2), (6, 2)), ((6, 7), (3, 7)), ((7, 1), (6, 1))]
'''

b4 = [('Knight', 'white', (3, 4)), 
      ('Knight', 'black', (7, 7)), 
      ('Knight', 'white', (0, 7)), 
      ('Knight', 'black', (7, 4)), 
      ('Combatant', 'white', (2, 2)), 
      ('Combatant', 'black', (1, 2)), 
      ('Combatant', 'white', (2, 7)), 
      ('Combatant', 'black', (7, 1)), 
      ('Combatant', 'white', (1, 4)), 
      ('Combatant', 'black', (6, 4)), 
      ('Combatant', 'white', (1, 1)), 
      ('Combatant', 'black', (5, 1)), 
      ('Bishop', 'white', (4, 1)), 
      ('Bishop', 'black', (0, 1)), 
      ('Squire', 'white', (6, 1)), 
      ('Squire', 'black', (1, 5)), 
      ('King', 'black', (0, 0)), 
      ('King', 'white', (7, 6))]
'''
get_legal_moves(b4, 'white') = [((7, 6), (6, 7)), ((4, 1), (5, 2)), ((1, 1), (2, 1)), ((1, 4), (0, 4)), ((2, 2), (2, 1)), ((7, 6), (6, 5)), ((7, 6), (7, 5)), ((1, 1), (1, 0)), ((1, 1), (0, 0)), ((7, 6), (7, 7)), ((6, 1), (5, 2)), ((6, 1), (7, 2)), ((2, 7), (3, 7)), ((2, 7), (2, 6)), ((3, 4), (5, 3)), ((2, 2), (2, 3)), ((0, 7), (2, 6)), ((4, 1), (3, 0)), ((3, 4), (2, 6)), ((4, 1), (6, 3)), ((4, 1), (2, 3)), ((2, 2), (3, 2)), ((6, 1), (7, 0)), ((1, 4), (1, 3)), ((4, 1), (3, 2)), ((6, 1), (6, 3)), ((3, 4), (1, 5)), ((6, 1), (5, 0)), ((3, 4), (4, 2)), ((3, 4), (4, 6)), ((3, 4), (1, 3)), ((4, 1), (7, 4)), ((1, 4), (2, 4)), ((3, 4), (5, 5)), ((2, 7), (1, 7)), ((7, 6), (6, 6)), ((4, 1), (5, 0)), ((0, 7), (1, 5))]
'''
#squire wins 
m1_1 = [("Combatant", 'white', (0,5)),
        ("Rook", "white", (1,1)),
        ("Combatant", "white", (1,4)),
        ("King", "black", (1,5)),
        ("Combatant", "white", (1,6)),
        ("Squire", "white", (1,7)),
        ("Combatant", "white", (2,5)),
        ("Rook", "black", (4,3)),
        ("King", "white", (5,2)),
        ("Rook", "white", (6,5)),
        ("Bishop", "black", (7,0)),
        ("Bishop", "black", (7,3))
        ]
'''
studentAgent(m1_1) = ((1, 7), (1, 5))
'''

m3_1 = [("King", 'white', (7,7)),
          ("King", 'black', (0,0)),
          ("Rook", 'white', (6,1)),
          ("Rook", 'white', (5,1)),
          ("Rook", 'black', (6,5)),
          ("Rook", 'black', (6,6))]
'''
studentAgent(m3_1) = ((5, 1), (5, 0))
'''

m5_1 = [("King", 'white', (2,3)),
          ("King", 'black', (0,4)),
          ("Combatant", 'white', (1,4)),
          ("Combatant", 'white', (2,5)),
          ("Combatant", 'black', (7,0))]
'''
studentAgent(m5_1) = ((2, 3), (2, 4))
'''

e3_1 = [("King", "black", (0,4)), 
        ("Rook", "black", (4,4)), 
        ("King", "white", (2,3)), 
        ("Squire", "white", (2,2))]
'''
studentAgent(e3_1) = ((2, 2), (2, 4))
'''

e3_2 = [("Rook", 'white', (0,2)),
        ("King", 'white', (1,2)),
        ("Rook", 'black', (3,0)),
        ("King", 'black', (6,2)),
        ("Rook", 'black', (6,4))]
'''
studentAgent(e3_2) = ((1, 2), (2, 1))
'''



answer = [((2, 4), (4, 5)), ((6, 3), (6, 2)), ((4, 2), (3, 3)), ((2, 4), (0, 3)), ((1, 3), (1, 1)), ((5, 6), (3, 7)), ((2, 2), (1, 2)), ((7, 5), (6, 6)), ((1, 3), (1, 5)), ((5, 4), (7, 6)), ((4, 2), (3, 1)), ((1, 3), (0, 4)), ((6, 3), (2, 3)), ((6, 3), (6, 5)), ((7, 4), (6, 5)), ((2, 4), (1, 2)), ((7, 5), (6, 5)), ((4, 2), (5, 1)), ((6, 3), (4, 3)), ((1, 6), (0, 7)), ((5, 4), (2, 1)), ((5, 4), (3, 2)), ((1, 6), (2, 7)), ((2, 4), (0, 5)), ((5, 4), (4, 5)), ((5, 4), (4, 3)), ((6, 3), (6, 6)), ((1, 3), (3, 3)), ((1, 3), (0, 2)), ((1, 6), (0, 5)), ((4, 2), (6, 0)), ((1, 6), (2, 5)), ((6, 3), (6, 0)), ((5, 6), (3, 5)), ((5, 6), (4, 4)), ((5, 4), (6, 5)), ((2, 2), (2, 1)), ((6, 3), (3, 3)), ((6, 3), (5, 3)), ((2, 2), (2, 3)), ((2, 2), (3, 1)), ((2, 4), (3, 2)), ((6, 3), (7, 3)), ((4, 2), (5, 3)), ((2, 4), (4, 3)), ((5, 4), (2, 7)), ((2, 2), (3, 2)), ((4, 2), (6, 4)), ((6, 3), (6, 4)), ((2, 4), (3, 6)), ((5, 4), (3, 6)), ((6, 3), (6, 1)), ((7, 4), (7, 3)), ((1, 6), (3, 6)), ((7, 5), (7, 6)), ((7, 4), (6, 4)), ((5, 6), (7, 7)), ((1, 6), (1, 4)), ((5, 6), (6, 4)), ((5, 4), (1, 0))]
answer = set(answer)
#my_ans = get_legal_moves(m3_1, 'white')
#print(my_ans)
l = [m1_1,m3_1,m5_1,e3_1,e3_2]
for b in l:
    print(studentAgent(b))
    print('count_val',count_val)
    print('count_e', count_e)