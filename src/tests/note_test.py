import unittest
from entities.note import Note
from entities.snippet import Snippet

class TestNote(unittest.TestCase):
    def setUp(self):
        self.testnote = Note(1, "test content for note")

    def test_note_is_initialized_correctly(self):
        self.assertEqual(str(self.testnote), "This is a test note")

