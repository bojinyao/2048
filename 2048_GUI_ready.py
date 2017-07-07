"""2048 Game Developed by Max Yao"""
import random

def Two_Or_Four(abstract_number = False):
    """Choose between 2(75%) or 4(25%) and report one"""
    i = random.randint(0, 3)
    if abstract_number:
        return [Number(2), Number(2), Number(2), Number(4)][i]
    return [2,2,2,4][i]

def Empty_Positions(nlst, default_item = 0):
    """Takes in a one level nested list and reports all coordinates
    that are the default items"""
    return [[r, c] for r in range(len(nlst)) for c in range(len(nlst[0])) if nlst[r][c] == default_item]

def Direction_Selection(direction):
    if direction == 'w':
        return 'up'
    elif direction == 'd':
        return 'right'
    elif direction == 'a':
        return 'left'
    elif direction == 's':
        return 'down'
    elif direction == 'q':
        return 'break'
    else:
        pass

def Value_Question_Prompt(question, error_message, pred):
    """A prompt question abstraction for Value related questions
    input 1: a question you want in String
    input 2: the error message you want to display in String
    input 3: a Predicate function (lambda ok) to filter the answer
    """
    temp = None
    while True:
        try:
            print(' ')
            temp = int(input(str(question)))
            if not pred(temp):
                raise ValueError
            return temp
            break
        except ValueError:
            print(' ')
            print(str(error_message))

def Yes_or_No_Prompt(question, when_yes = True, when_no = False):
    """A prompt question abstraction for Yes/No related questions
    input 1: a question you want in String
    input 2: does YES imply True or False? (defaul to True)
    input 3: deos NO imply False or True? (default to False)
    """
    temp = None
    while True:
        try:
            print(' ')
            temp = str(input("{} (y/n): ".format(question)))
            if temp == 'y':
                temp = when_yes
            elif temp == 'n':
                temp = when_no
            else:
                raise ValueError
            return temp
            break
        except ValueError:
            print(' ')
            print('Please only type in "y" or "n"')

class Number:
    """A number abstraction
    Everything works similarly like integers,
    this serves as a level of abstraction to name
    integers and making sure that nothing but integers
    will be used
    """
    def __init__(self, integer):
        assert type(integer) is int and integer % 2 == 0
        self.integer = integer
        self.name = str(self.integer)

    def __repr__(self):
        # return "Number({0})".format(self.integer)
        return str(self.integer)

    def __str__(self):
        return str(self.integer)

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.integer + other.integer)
        return Number(self.integer + other)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.integer * other.integer)
        return Number(self.integer * other)

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.integer == other.integer
        return self.integer == other

class Game_Board:
    """A board object that creates a new board with two random positions
    filled with either 2 or 4"""
    def __init__(self, row = 4, column = 4, board = [[0 for _ in range(4)] for _ in range(4)]):
        self.row = row
        self.column = column
        self.board = board
        self.score = Number(0)
        for _ in range(2):
            empty_positions = Empty_Positions(self.board, Number(0))
            e1 = random.randint(0, len(empty_positions) - 1)
            r, c = empty_positions[e1]
            self.board[r][c] = Two_Or_Four(True)

    def __repr__(self):
        return str(self.board)

    def __len__(self):
        return len(self.board)

    def New_Element(self):
        """Add a new element (2 or 4) to the game board
        that is NOT FILLED"""
        empty_positions = Empty_Positions(self.board, Number(0))
        if empty_positions:
            e1 = random.randint(0, len(empty_positions) - 1)
            r, c = empty_positions[e1]
            self.board[r][c] = Two_Or_Four(True)
        else:
            pass

    def Select_Row(self, row):
        """return a new list of all items in row of board"""
        return self.board[row][:]

    def Select_Column(self, column):
        """Return a new list of all items in column of board"""
        return [self.board[i][column] for i in range(self.column)]

    def Update_New_Column(self, lst, column):
        for i in range(self.column):
            self.board[i][column] = lst[i]

    def Update_New_Row(self, lst, row):
        self.board[row] = lst

    def Merge_Column_or_Row(self, index, direction):
        """Merge a single column or row in a list: UP, DOWN, RIGHT, or LEFT
        No Side-effect
        return a 0 level list"""
        assert direction in ('up', 'down', 'right', 'left')
        if direction in ('up', 'down'):
            target = self.Select_Column(index)
        elif direction in ('right', 'left'):
            target = self.Select_Row(index)

        if direction == 'up' or direction == 'left':
            # target = Move_Up_Down(Merge_Up(Move_Up_Down(target, 'up')), 'up')
            target, temp = Merge_Up(Move_Up_Down(target, 'up'))
            target = Move_Up_Down(target, 'up')
            self.score += temp
        if direction == 'down' or direction == 'right':
            # target = Move_Up_Down(Merge_Down(Move_Up_Down(target, 'down')), 'down')
            target, temp = Merge_Down(Move_Up_Down(target, 'down'))
            target = Move_Up_Down(target, 'down')
            self.score += temp

        if direction in ('up', 'down'):
            self.Update_New_Column(target, index)
        elif direction in ('right', 'left'):
            self.Update_New_Row(target, index)

    def Merge(self, direction):
        """Merge all column in a nest list
        Side-effect on the original board"""
        assert direction in ('up', 'down', 'right', 'left')
        if direction in ('up', 'down'):
            for i in range(self.row):
                self.Merge_Column_or_Row(i, direction)
        elif direction in ('right', 'left'):
            for i in range(self.column):
                self.Merge_Column_or_Row(i, direction)

    def Copy(self):
        return [item[:] for item in self.board]

    def Print_Board(self):
        print("Score: {0}".format(self.score))
        for item in self.board:
            print(item)

    def Game_Over(self):
        """If there is no moves left (dead) this turns True, else False"""
        if Empty_Positions(self.board):
            return False
        copy = self.Copy()
        mock_board = Test_Board(self.row, self.column, copy)
        for item in ('up', 'down', 'right', 'left'):
            mock_board.Merge(item)
            if mock_board.board != self.board:
                return False
        return True


"""NOTE: Merging up is the same as Merging Left"""
def Move_Up_Down(lst, direction):
    """Moving a single column UP in a 0 level list
    No Side-effect
    return a 0 level list"""
    assert direction in ('up', 'down')
    length = len(lst)
    result = [num for num in lst if num != Number(0)]
    result_length = len(result)
    for _ in range(abs(length - result_length)):
        if direction == 'up':
            result.append(Number(0))
        if direction == 'down':
            result.insert(0, Number(0))
    return result

"""Score is incremented based on Merge
Below is a working version"""
def Merge_Up(lst):
    copy = lst[:]
    score = Number(0)
    for i in range(1, len(lst)):
        if copy[i - 1] == copy[i]:
            copy[i - 1] *= 2
            score += copy[i - 1]
            copy[i] = Number(0)
    return copy, score

def Merge_Down(lst):
    copy = lst[:]
    score = Number(0)
    i = len(lst) - 1
    while i > 0:
        if copy[i - 1] == copy[i]:
            copy[i] *= 2
            score += copy[i]
            copy[i - 1] = Number(0)
            i -= 1
        else:
            i -= 1
    return copy, score


class Test_Board(Game_Board):
    """A Tester to test functions of the Game_Board"""
    def __init__(self, row = 4, column = 4, board = [[0, 2, 0, 2], [2, 2, 2, 2], [2, 0, 0, 2], [0, 0, 0, 4]]):
        self.board = board
        self.row = row
        self.column = column
        self.score = Number(0)



# class GUI_Board:
#     def __init__(self, game_board):
#         self.row = game_board.row
#         self.column = game_board.column
#         self.game_board = game_board

Tester1 = [[2,4,2,4], [4,2,4,2], [2,4,2,4], [4,2,4,2]]
Tester2 = [[0,16,32,40], [48,56,64,72], [80,88,96,104], [112,120,128,136]]
Tester3 = [[0, 0, 2, 0], [2, 2, 0, 2], [0, 2, 2, 2], [2, 4, 2, 8]]
Tester4 = [[2,2,2,2], [2,2,2,2], [2,2,2,2], [2,2,2,2]]
Num_Tester= [[Number(2048), Number(1024), Number(512), Number(256)],
            [Number(16), Number(32), Number(64), Number(128)],
            [Number(8), Number(4), Number(2), Number(2)],
            [Number(2), Number(2), Number(2), Number(2)]
            ]

"""Game Logic"""
def Play_2048(num_of_row = 4, num_of_column = 4, tester = None):
    assert type(num_of_row) is int and num_of_row > 1
    assert type(num_of_column) is int and num_of_column > 1
    if tester is None:
        main = Game_Board(num_of_row, num_of_column, [[Number(0) for _ in range(num_of_row)] for _ in range(num_of_column)])
    else:
        main = Test_Board(num_of_row, num_of_column, tester)
    last_board = []
    # print('before merge main board', main.board)
    # print('before merge last board', last_board)
    main.Print_Board()
    while not main.Game_Over():
        while True:
            try:
                temp = str(input())
                if temp not in ('w', 'a', 's', 'd', 'q'):
                    raise ValueError
                break
            except ValueError:
                pass
        direction = Direction_Selection(temp)
        if direction == 'break':
            break
        main.Merge(direction)
        # print('after merge main board', main.board)
        # print('after merge last board', last_board)
        if main.board != last_board:
            main.New_Element()
            # print('New element')
            last_board = main.Copy()
        main.Print_Board()
    print('This Round is Over')

"""Play Game"""
STANDARD_GAME = Yes_or_No_Prompt("Play standard 4 x 4 2048 Game?")
if STANDARD_GAME:
    Play_2048(4,4)
else:
    ROW = Value_Question_Prompt("How many vertical rows do you want? (y > 1): ", "Check input", lambda y: y > 1)
    COLUMN = Value_Question_Prompt("How many horizontal columns do you want? (x > 1): ", "Check input", lambda x: x > 1)
    Play_2048(ROW, COLUMN)
# Play_2048(4,4)
