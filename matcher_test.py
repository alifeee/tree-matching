"""tests for matcher.py"""

import unittest
from matcher import Board, Plate, board_is_valid, connection_is_valid


class TestPlate(unittest.TestCase):
    """test Plate class"""

    def test_rotated(self):
        """test rotated method"""
        p = Plate("A", "abcdef")
        self.assertEqual(p.rotated(0), Plate("A", "abcdef"))
        self.assertEqual(p.rotated(1), Plate("A", "bcdefa"))
        self.assertEqual(p.rotated(2), Plate("A", "cdefab"))
        self.assertEqual(p.rotated(3), Plate("A", "defabc"))
        self.assertEqual(p.rotated(4), Plate("A", "efabcd"))
        self.assertEqual(p.rotated(5), Plate("A", "fabcde"))


class TestConnectionIsValid(unittest.TestCase):
    """test connection_is_valid method"""

    def test_connection_is_valid(self):
        """test connectionIsValid method"""
        plate1 = Plate("A", "abcdef")
        plate2 = Plate("B", "bcdefa")

        self.assertFalse(connection_is_valid(plate1, plate2, 1, 1))
        self.assertTrue(connection_is_valid(plate1, plate2, 1, 6))
        self.assertTrue(connection_is_valid(plate1, plate2, 2, 1))

    def test_connection_is_valid_with_rotated(self):
        """test with rotated plates"""
        plate1 = Plate("A", "abcdef")
        plate2 = Plate("B", "bcdefa")

        plate1rot = plate1.rotated(1)

        self.assertTrue(connection_is_valid(plate1rot, plate2, 1, 1))


class TestBoardIsValid(unittest.TestCase):
    """test board_is_valid method"""

    def test_board_is_invalid(self):
        """test board_is_valid method"""
        plate1 = Plate("A", "abcdef")
        plate2 = Plate("B", "bcdefa")
        plate3 = Plate("C", "cdefab")

        board = Board([plate1, plate2, plate3])

        self.assertFalse(board_is_valid(board))

    def test_one_tile_is_valid(self):
        """test board_is_valid method"""
        plate1 = Plate("A", "abcdef")

        board = Board([plate1])

        self.assertTrue(board_is_valid(board))

    def test_two_tiles_are_valid(self):
        """test board_is_valid method"""
        plate1 = Plate("A", "abcdef")
        plate2 = Plate("B", "defabc")

        board = Board([plate1, plate2])

        self.assertTrue(board_is_valid(board))

    def test_three_tiles_are_valid(self):
        """test board_is_valid method"""
        plate1 = Plate("A", "abcdef")
        plate2 = Plate("B", "defabc")
        plate3 = Plate("C", "aecdbf")

        board = Board([plate1, plate2, plate3])

        self.assertTrue(board_is_valid(board))
