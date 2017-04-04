"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] == 0:
            if target_col < self._width - 1:
                for col in range(target_col + 1, self._width):
                    if self._grid[target_row][col] != ((target_row + 1) * self._width) - (self._width - col):
                        return False
            if target_row < self._height - 1:
                for col2 in range(self._width):
                    if self._grid[target_row + 1][col2] != ((target_row + 2) * self._width) - (self._width - col2):
                        return False
                    else:
                        return True
            else:
                return True
        else:
            return False
    
    def final_0_pos(self, zero_pos, end_zero_pos):
        """
        Returns move to place 0 in final position to satisfy invariants
        """
        print end_zero_pos
        
        v_dist = abs(zero_pos[0] - end_zero_pos[0])
        h_dist = abs(zero_pos[1] - end_zero_pos[1])
        move = ""
        total_moves = ""
        done = False
        while not done:
            if zero_pos[0] > end_zero_pos[0]:
                for dummy_move in range(v_dist):
                    move += "u"
                total_moves += move
                self.update_puzzle(move)
                move = ""
                zero_pos = self.current_position(0, 0)
            elif zero_pos[0] < end_zero_pos[0]:
                for dummy_move in range(end_zero_pos[0] - zero_pos[0]):
                    move += "d"
                total_moves += move
                self.update_puzzle(move)
                move = ""
                zero_pos = self.current_position(0, 0)
            elif zero_pos[1] != end_zero_pos[1]:
                if zero_pos[1] > end_zero_pos[1]:
                    for dummy_move in range(h_dist):
                        move += "l"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    zero_pos = self.current_position(0, 0)
                elif zero_pos[1] < end_zero_pos[1]:
                    for dummy_move in range(h_dist):
                        move += "r"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    zero_pos = self.current_position(0, 0)
            
            if zero_pos[0] == end_zero_pos[0]:
                if zero_pos[1] == end_zero_pos[1]:
                    done = True
            
        return total_moves
                    
    def position_tile(self, target_row, target_col, end_loc = None, end_zero_pos = None):
        """
        Returns a sequence of moves to position target tile in targeted space
        """
        def is_zero_below(zero_pos, location):
            """
            Checks whether zero in position below target tile. Returns a boolean.
            """
            if zero_pos[1] == location[1]:
                return True
            else:
                return False
        
        def update(self, move):
            """
            Updates puzzle with given move.
            """
            self.update_puzzle(move)
            return move
        
        if end_loc == None:
            end_loc = (target_row, target_col)
        if end_zero_pos == None:
            end_zero_pos = [target_row, target_col - 1]
            
        move = ""
        total_moves = ""
        location = self.current_position(target_row, target_col)
        zero_pos = self.current_position(0, 0)
        
        while location != end_loc:
            location = self.current_position(target_row, target_col)
            zero_pos = self.current_position(0, 0)
            
            # x in correct col
            if location[1] == end_loc[1] and location[0] != end_loc[0]:
                v_dist = abs(zero_pos[0] - location[0])
                for dummy_move in range(v_dist):
                    move += "u"
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                
                if is_zero_below(zero_pos, location):
                    move += "ld"
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                    
                # reposition 0 under x
                if location[0] != end_loc[0]:
                    if location[0] > end_loc[0]:
                        if zero_pos[0] == location[0]:
                            if zero_pos[1] == location[1] - 1:
                                move += "urd"
                            elif zero_pos[1] == location[1] + 1:
                                move += "uld"
                    elif location[0] < end_loc[0]:
                        if zero_pos[1] > location[1]:
                            if zero_pos[0] != 0:
                                move += "ullddr"
                            else:
                                move += "dl"
                        else:
                            move += "dr"
                    total_moves += update(self, move)
                    move = ""
                    location = self.current_position(target_row, target_col)
                    zero_pos = self.current_position(0, 0)
                        
            # if x not in correct col    
            elif location[1] != end_loc[1]:
                if location[0] < zero_pos[0]:
                    v_dist = abs(zero_pos[0] - location[0])
                    for dummy_move in range(v_dist):
                        move += "u"
                    total_moves += update(self, move)
                    move = ""
                    location = self.current_position(target_row, target_col)
                    zero_pos = self.current_position(0, 0)
                
                if location[1] > zero_pos[1] and location[1] > end_loc[1]:
                    for dummy_move in range(abs(location[1] - zero_pos[1])):
                        move += "r"
                elif location[1] < zero_pos[1] and location[1] < end_loc[1]:
                    for dummy_move in range(abs(location[1] - zero_pos[1])):
                        move += "l"
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                
                # if col is wrong
                if location[1] < zero_pos[1] and location[1] != end_loc[1]:
                    move += "ul"
                    if location[1] != end_loc[1]:
                        move += "ld"
                elif location[1] > zero_pos[1] and location[1] != end_loc[1]:
                    move += "ur"
                    if location[1] != end_loc[1]:
                        move += "rd"
                
                # if top row
                if location[0] == 0:
                    move = move.replace("d", "u")
                    move = move.replace("u", "d", 1)
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                    
                if location[0] > zero_pos[0]:
                    move += "ld"
                    if location[1] == 0:
                        move = move.replace("l", "r")

            total_moves += update(self, move)
            move = ""
            location = self.current_position(target_row, target_col)
            zero_pos = self.current_position(0, 0)
        
        # getting 0 into final position to satisfy invariants   
        if location == (end_loc) and zero_pos != end_zero_pos:
            total_moves += self.final_0_pos(zero_pos, end_zero_pos) 
        
        return total_moves
        
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row > 1
        assert target_col > 0
        assert self.lower_row_invariant(target_row, target_col)

        move_sequence = self.position_tile(target_row, target_col)

        assert self.lower_row_invariant(target_row, target_col -1)
        return move_sequence


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        
        location = self.current_position(target_row, 0)
        zero_pos = [target_row, 0]
        total_moves = ""
        move = ""
        
        while location != (target_row, 0):
            skip = False
            location = self.current_position(target_row, 0)
            if location == (target_row - 1, 0):
                move = "u"
                zero_pos[0] -= 1
                skip = True
            elif location == (target_row - 1, 1):
                move = "urulddrulurddlur"
                zero_pos = [target_row - 1, 1]
                skip = True
            if zero_pos[1] != self._width - 1 and location == (target_row, 0):
                dist = (self._width - 1) - zero_pos[1]
                for dummy_move in range(dist):
                    move += "r"
                zero_pos[1] = self._width - 1
                skip = True
                            
            if not skip:
                if location != (target_row - 1, 1) and location != (target_row, 0):
                    total_moves += self.position_tile(target_row, 0, (target_row - 1, 1), (target_row, 0))
                        
            total_moves += move
            self.update_puzzle(move)
            move = ""
        
        assert self.lower_row_invariant(target_row - 1, self._width - 1)
        return total_moves
                    

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0:
            return False
        
        portion = 1
        for idx in range(2):
            right = self._grid[idx]
            col = len(right[target_col + portion:])
            for val in right[target_col + portion:]:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
            portion -= 1
        
        for idx in range(2, self._height):
            row = self._grid[idx]
            col = self._width
            for val in row:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
                
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False
        
        for idx in range(2):
            right = self._grid[idx]     
            col = len(right[target_col + 1:])
            for val in right[target_col + 1:]:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
                
        for idx in range(2, self._height):
            row = self._grid[idx]
            col = self._width
            for val in row:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
                
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        
        location = self.current_position(0, target_col)
        zero_pos = self.current_position(0, 0)
        total_moves = ""
        move = ""
        
        while location != (0, target_col):
            if location[0] == 0 and location[1] == target_col - 1 and self.row0_invariant(target_col):
                move += "ld"
                self.update_puzzle(move)
                total_moves += move
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
                break
          
            if location[0] > zero_pos[0] and location[1] < zero_pos[1]:
                for dummy_move in range(zero_pos[1] - location[1]):
                    move += "l"
                for dummy_move in range(abs(zero_pos[0] - location[0])):
                    move += "d"
                total_moves += move
                self.update_puzzle(move)
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
            
                if location[1] != target_col - 1:
                    move += "ruldr"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    location = self.current_position(0, target_col)
                    zero_pos = self.current_position(0, 0)
              
            if location[0] == 0 and location[1] == target_col - 1:
                move += "uldrurdluldruldrruld"
                self.update_puzzle(move)
                total_moves += move
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
            
            else:
                move_sequence = self.position_tile(0, target_col, (0, target_col - 1), (1, target_col - 1))
                total_moves += move_sequence
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
               
        assert self.row1_invariant(target_col - 1)
        return total_moves

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        
        move_sequence = self.position_tile(1, target_col, None, (0, target_col))
        
        assert self.row0_invariant(target_col)
        
        return move_sequence

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        
        total_moves = ""
        sequence = ["l", "u", "r", "d"]
        
        row0 = [val for val in range(self._width)]
        row1 = [val + self._width for val in range(self._width)]
        
        while self._grid[0] != row0 and self._grid[1] != row1:
            for move in sequence:
                total_moves += move
                self.update_puzzle(move)
                if self._grid[0] == row0 and self._grid[1] == row1:
                    break
                    
        return total_moves

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        def solved(self, solved_puzzle):
            """
            Checks the current grid with the solved grid; returns True when puzzle is solved
             """
            if self._grid == solved_puzzle:
                return True
            else:
                return False
            
        solved_puzzle = [[col + (self._width * row) for col in range(self._width)] for row in range(self._height)]
        total_moves = ""
        move = ""
        zero_pos = self.current_position(0, 0)
        
        if not solved(self, solved_puzzle):
            not_solved = None
            for row in range(self._height - 1, -1, -1):
                if self._grid[row] != solved_puzzle[row]:
                    not_solved = row
                    break
                
            idx = ()  
            for col in range(self._width):
                if (not_solved, col) != self.current_position(not_solved, col):
                    idx = (not_solved, col)
          
            while zero_pos != idx:
                if zero_pos[1] > idx[1] or zero_pos[1] < idx[1]:
                    for dummy_move in range(abs(zero_pos[1] - idx[1])):
                        if zero_pos[1] > idx[1]:
                            move += "l"
                        else:
                            move += "r"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    zero_pos = self.current_position(0, 0)
                if zero_pos[0] < idx[0] or zero_pos[0] > idx[0]:
                    for dummy_move in range(abs(zero_pos[0] - idx[0])):
                        if zero_pos[0] < idx[0]:
                            move += "d"
                        else:
                            move += "u"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    zero_pos = self.current_position(0, 0)
                
            if zero_pos[0] == 1:
                if not self.row1_invariant(zero_pos[1]):
                    move += "ur"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    zero_pos = self.current_position(0, 0)
          
            while not solved(self, solved_puzzle):
                if zero_pos[0] > 1 and zero_pos[1] != 0:
                    total_moves += self.solve_interior_tile(zero_pos[0], zero_pos[1])
                zero_pos = self.current_position(0, 0)
                if zero_pos[0] > 1 and zero_pos[1] == 0:
                    total_moves += self.solve_col0_tile(zero_pos[0])
                zero_pos = self.current_position(0, 0)
                if zero_pos[0] == 1 and zero_pos[1] > 1:
                    total_moves += self.solve_row1_tile(zero_pos[1])
                zero_pos = self.current_position(0, 0)
                if zero_pos[0] == 0 and zero_pos[1] > 1:
                    total_moves += self.solve_row0_tile(zero_pos[1])
                zero_pos = self.current_position(0, 0)
                if zero_pos == (1, 1):
                    total_moves += self.solve_2x2()
                zero_pos = self.current_position(0, 0)

        return total_moves
                  

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

#game = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#game = Puzzle(4, 4, [[1, 2, 11, 3], [8, 6, 10, 0], [12, 15, 5, 14], [4, 9, 13, 7]])
#game = Puzzle(4, 4, [[5, 4, 3, 0], [1, 10, 2, 9], [8, 6, 11, 7], [12, 13, 14, 15]])
#game2 = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#game = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print game.solve_2x2()
#print game.solve_puzzle()
#poc_fifteen_gui.FifteenGUI(game)