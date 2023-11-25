"""matcher!"""


from typing import Any, List, Tuple
import re


class Plate:
    """A hexagonal plate with a label (centre) and a layout of images
    represented as lowercase letters, e.g., "abcdef"
    """

    def __init__(self, label: str, layout: str):
        self.label = label
        self.layout = layout

    def __repr__(self):
        return f"{self.label} ({self.layout})"

    def __str__(self):
        return self.__repr__()

    def rotated(self, n: int) -> "Plate":
        """Return a new plate with the layout rotated n times anticlockwise"""
        return Plate(self.label, self.layout[n:] + self.layout[:n])

    def __eq__(self, other):
        return self.label == other.label and self.layout == other.layout

    def __hash__(self):
        return hash(self.label + self.layout)

    def __getitem__(self, position):
        """Return the character at position"""
        return self.layout[position]


BOARD_ASCII = """
           54   
        55     53
   64    56     52    44
65     63    51    45     43
66     62    14    46     42
   61    15     13    41
   74    16     12    34
75     73    11    35     33
76     72    24    36     32
   71    25     23    31
        26     22
           21    
"""

BOARD_ASCII_SIMPLE = """
    5
6       4
    1
7       3
    2
"""


class Board:
    """A board of hexagonal plates"""

    def __init__(self, plates: List[Plate]):
        self.plates = plates

    def __repr__(self):
        return f"Board({self.plates})"

    def __str__(self):
        return self.__repr__()

    def ascii(self):
        """pretty print"""
        _board = BOARD_ASCII
        for i, plate in enumerate(self.plates):
            for j, char in enumerate(plate.layout):
                _board = _board.replace(f"{i+1}{j+1}", char)
        # replace any remaining digit pairs with spaces
        _board = re.sub(r"\d\d", " ", _board)
        return _board

    def ascii_simple(self):
        """pretty print"""
        _board = BOARD_ASCII_SIMPLE
        for i, plate in enumerate(self.plates):
            _board = _board.replace(f"{i+1}", plate.label)
        _board = re.sub(r"\d", " ", _board)
        return _board

    def __eq__(self, other):
        return self.plates == other.plates

    def __hash__(self):
        return hash(self.plates)

    def __len__(self):
        return len(self.plates)

    def __getitem__(self, position):
        return self.plates[position - 1]

    def __add__(self, other: Plate):
        return Board(self.plates + [other])


def connection_is_valid(plate1, plate2, position1, position2):
    """Return True if the connection between plate1 and plate2 is valid,
    i.e., the character of plate1 matches the character of plate2 at the
    connection point
    """
    return plate1[position1 - 1] == plate2[position2 - 1]


def board_is_valid(board):
    """Return True if the board is valid, i.e., the layout of each plate matches the layout of the adjacent plates"""
    valid = True
    if len(board) >= 2:
        # 1<->2 1<->4
        valid = valid and connection_is_valid(board[1], board[2], 1, 4)
    if len(board) >= 3:
        # 1<->3 2<->5
        # 2<->3 3<->6
        valid = valid and connection_is_valid(board[1], board[3], 2, 5)
        valid = valid and connection_is_valid(board[2], board[3], 3, 6)
    if len(board) >= 4:
        # 1<->4 3<->6
        # 3<->4 4<->1
        valid = valid and connection_is_valid(board[1], board[4], 3, 6)
        valid = valid and connection_is_valid(board[3], board[4], 4, 1)
    if len(board) >= 5:
        # 1<->5 4<->1
        # 4<->5 5<->2
        valid = valid and connection_is_valid(board[1], board[5], 4, 1)
        valid = valid and connection_is_valid(board[4], board[5], 5, 2)
    if len(board) >= 6:
        # 1<->6 5<->2
        # 5<->6 6<->3
        valid = valid and connection_is_valid(board[1], board[6], 5, 2)
        valid = valid and connection_is_valid(board[5], board[6], 6, 3)
    if len(board) >= 7:
        # 1<->7 6<->3
        # 6<->7 1<->4
        # 7<->2 2<->5
        valid = valid and connection_is_valid(board[1], board[7], 6, 3)
        valid = valid and connection_is_valid(board[6], board[7], 1, 4)
        valid = valid and connection_is_valid(board[7], board[2], 2, 5)

    return valid


def board_is_complete(board):
    """Return True if the board is complete, i.e., all plates are used"""
    return len(board) == 7


def next_board(board: Board, plate_options: List[Plate]) -> Tuple[bool, Board]:
    """recursive function"""
    # board is complete
    if plate_options == []:
        return True, board

    # print()
    # print("NEW FUNCTION CALL")
    # print("current board:", board)
    # print("current plate options:", plate_options)
    next_boards = []
    next_plates = []
    for plate_option in plate_options:
        rotated_plates = [plate_option.rotated(i) for i in range(6)]
        for rotated_plate in rotated_plates:
            # print("testing plate:", rotated_plate, "on board:", board)
            new_board = board + rotated_plate
            new_plate_options = plate_options.copy()
            new_plate_options.remove(plate_option)

            if board_is_valid(new_board):
                next_boards.append(new_board)
                next_plates.append(new_plate_options)

    for i, _ in enumerate(next_boards):
        valid, board = next_board(next_boards[i], next_plates[i])
        if valid:
            return True, board

    return False, board


def main():
    """main"""
    plate1 = Plate("A", "abfced")
    plate2 = Plate("B", "adebcf")
    plate3 = Plate("C", "afcdbe")
    plate4 = Plate("D", "adfbec")
    plate5 = Plate("E", "adecfb")
    plate6 = Plate("F", "abcdef")
    plate7 = Plate("G", "acbdef")

    board = Board([])

    plate_options = [plate1, plate2, plate3, plate4, plate5, plate6, plate7]

    valid, final_board = next_board(board, plate_options)
    if valid:
        print("solution found")
        print(final_board)
        print(final_board.ascii_simple())
        print(final_board.ascii())


if __name__ == "__main__":
    main()
