import unittest
from note import Note
from snippet import Snippet

class TestNote(unittest.TestCase):
    def setUp(self):
        self.testnote = Note()

    def test_note_is_initialized_correctly(self):
        self.assertEqual(vastaus, "Kortilla on rahaa 10 euroa")

