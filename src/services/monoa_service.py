'''
Main module for handling notes and snips between UI and DB
- provides up-to-date lists of snips and notes
- keeps the lists sorted by timestamp, latest first
'''
from datetime import datetime
from entities.note import Note
#from entities.snip import Snip
import database.db_handler as db_handler

class MonoaService:
    '''
    Main content handler class
    '''
    def __init__(self):
        ''' Load all notes and snippets to lists '''
        self.notes = list()
        self.notesdict = dict()
        self._load_notes()

    def create_note(self, n_name: str, n_content: str, n_timestamp: datetime) -> Note:
        ''' Create new note: '''
        note = db_handler.create_note(n_name, n_content, n_timestamp)
        self._load_notes()
        self._sort_notes()
        return self.get_note_by_id(note['id'])

    def update_note(self, note: Note) -> None:
        ''' Update note in database '''
        db_handler.update_note(
            note.get_id(),
            note.get_name(),
            note.get_content(),
            note.get_timestamp()
        )
        self._load_notes()
        self._sort_notes()

    def get_notes(self) -> list:
        ''' Return notes '''
        self._sort_notes()
        return self.notes

    def get_latest_note_id(self) -> int:
        self._sort_notes()
        return int(self.notes[0].get_id())


    def get_note_by_id(self, n_id: int) -> Note:
        ''' Return note by id '''
        for note in self.notes:
            if note.get_id() == n_id:
                return note

    def _load_notes(self) -> None:
        ''' Load all notes from database repository '''
        self.notes.clear()
        for note in db_handler.load_notes():
            self.notes.append(
                Note(
                    note['id'],
                    note['name'],
                    note['content'],
                    note['timestamp']
                )
            )
        self._sort_notes()

    def _sort_notes(self) -> None:
        ''' Keep self.notes sorted descending by the timestamp'''
        notes_sortable = dict()
        for note in self.notes:
            notes_sortable[note.get_timestamp()] = note
        self.notes.clear()
        for key, value in sorted(notes_sortable.items(), reverse=True):
            self.notes.append(value)

    """
    def create_snip(self, s_name: str, s_content: str):
        ''' Create new snippet: '''
        snip = db_handler.create_snip(s_name, s_content)
        self.snips.append(
            Snip(snip['id'], snip['name'], snip['content'], snip['timestamp'])
        )
        self._sort_snips()

    def update_snip(self, s_id: int, s_name: str, s_content: str) -> None:
        ''' Update snip by the given id '''
        if db_handler.update_snip(s_id, s_name, s_content):
            self._load_snips()
        else:
            print("Could not save to database!")
        self._sort_snips()

    def get_snips(self):
        ''' Return list of snippets '''
        return self.snips

    def get_snip_by_id(self, s_id: int):
        ''' Return snippet by id '''
        result = None
        for snip in self.snips:
            if snip.get_id() == s_id:
                result = snip
        return result

    def _load_snips(self) -> None:
        ''' Load snippets from database repository '''
        snips = db_handler.load_snips()
        for snip in snips:
            self.snips.append(
                Snip(snip['id'], snip['name'], snip['content'], snip['timestamp'])
            )
        self._sort_snips()

    def _sort_snips(self) -> None:
        ''' Keep self.snips sorted descending by the timestamp'''
        snips_sortable = dict()
        for snip in self.snips:
            snips_sortable[snip.get_timestamp()] = snip
        self.snips.clear()
        for key, value in sorted(snips_sortable.items(), reverse=True):
            self.snips.append(value)
    """

# One and only instance of this class
monoa_service = MonoaService()
