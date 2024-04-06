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
            return 40  # Lowest value
    def update_pos(self, new_pos):
        # Create a new instance of the current class with updated position
        return self.__class__(self.color, new_pos)
    
    def __repr__(self):
        return f"{self.name}, {self.color}, {self.position}"


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

def get_legal_moves(gameboard , color):
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
                    check.append([(x,y),new_s])
                else:
                    capture.append([(x,y),new_s])
            else:
                new_m = [z for z in m_pieces if z.position != p.position]
                up_p = p.update_pos(y)
                new_m.append(up_p)
                new_o = o_pieces.copy()
                new_s = new_m + new_o
                nochange.append([(x,y),new_s])
    total = check + capture + nochange
    return total
    
pieces = setUpBoard(b2)
states = create_state(pieces, "white")
s1 = get_legal_moves(b2, "white")
answers = [((2, 4), (4, 5)), ((6, 3), (6, 2)), ((4, 2), (3, 3)), ((2, 4), (0, 3)), ((1, 3), (1, 1)), ((5, 6), (3, 7)), ((2, 2), (1, 2)), ((7, 5), (6, 6)), ((1, 3), (1, 5)), ((5, 4), (7, 6)), ((4, 2), (3, 1)), ((1, 3), (0, 4)), ((6, 3), (2, 3)), ((6, 3), (6, 5)), ((7, 4), (6, 5)), ((2, 4), (1, 2)), ((7, 5), (6, 5)), ((4, 2), (5, 1)), ((6, 3), (4, 3)), ((1, 6), (0, 7)), ((5, 4), (2, 1)), ((5, 4), (3, 2)), ((1, 6), (2, 7)), ((2, 4), (0, 5)), ((5, 4), (4, 5)), ((5, 4), (4, 3)), ((6, 3), (6, 6)), ((1, 3), (3, 3)), ((1, 3), (0, 2)), ((1, 6), (0, 5)), ((4, 2), (6, 0)), ((1, 6), (2, 5)), ((6, 3), (6, 0)), ((5, 6), (3, 5)), ((5, 6), (4, 4)), ((5, 4), (6, 5)), ((2, 2), (2, 1)), ((6, 3), (3, 3)), ((6, 3), (5, 3)), ((2, 2), (2, 3)), ((2, 2), (3, 1)), ((2, 4), (3, 2)), ((6, 3), (7, 3)), ((4, 2), (5, 3)), ((2, 4), (4, 3)), ((5, 4), (2, 7)), ((2, 2), (3, 2)), ((4, 2), (6, 4)), ((6, 3), (6, 4)), ((2, 4), (3, 6)), ((5, 4), (3, 6)), ((6, 3), (6, 1)), ((7, 4), (7, 3)), ((1, 6), (3, 6)), ((7, 5), (7, 6)), ((7, 4), (6, 4)), ((5, 6), (7, 7)), ((1, 6), (1, 4)), ((5, 6), (6, 4)), ((5, 4), (1, 0))]


