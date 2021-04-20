'''
Main module for handling notes and snips between UI and DB
- provides up-to-date lists of snips and notes
- keeps the lists sorted by timestamp, latest first
'''
from entities.note import Note
from entities.snip import Snip
import database.db_handler as db_handler

class MonoaService:
    '''
    Main content handler class
    '''
    def __init__(self):
        ''' Load all notes and snippets to lists '''
        self.notes = []
        self.snips = []
        self._load_notes()
        self._load_snips()
        self._sort_snips()
        self._sort_notes()

    def create_snip(self, s_name: str, s_content: str):
        ''' Create new snippet: '''
        snip = db_handler.create_snip(s_name, s_content)
        self.snips.append(
            Snip(snip['id'], snip['name'], snip['content'], snip['timestamp'])
        )
        self._sort_snips()

    def update_snip(self, s_id: int, s_name: str, s_content: str):
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

    def create_note(self, n_name: str, n_content: str):
        ''' Create new note: '''
        note = db_handler.create_note(n_name, n_content)
        self.notes.append(
            Note( note['id'], note['name'], note['content'], note['timestamp'])
        )
        self._sort_notes()

    def update_note(self, n_id: int, n_name: str, n_content: str):
        ''' Update note in database '''
        if db_handler.update_note(n_id, n_name, n_content):
            self._load_notes()
        else:
            print("Could not save to database!")
        self._sort_notes()

    def get_notes(self):
        ''' Return list of notes '''
        return self.notes

    def get_note_by_id(self, n_id: int):
        ''' Return note by id '''
        result = None
        for note in self.notes:
            if note.get_id() == n_id:
                result = note
        return result

    def _load_snips(self):
        ''' Load snippets from database repository '''
        snips = db_handler.load_snips()
        for snip in snips:
            self.snips.append(
                Snip(snip['id'], snip['name'], snip['content'], snip['timestamp'])
            )
        self._sort_snips()

    def _load_notes(self):
        ''' Load all notes from database repository '''
        notes = db_handler.load_notes()
        for note in notes:
            self.notes.append(
                Note(note['id'], note['name'], note['content'], note['timestamp'])
            )
        self._sort_notes()

    def _sort_snips(self):
        ''' Keep self.snips sorted descending by the timestamp'''
        snips_sortable = dict()
        for snip in self.snips:
            snips_sortable[snip.get_timestamp()] = snip
        self.snips.clear()
        for snip in sorted(snips_sortable.values(), reverse=True):
            self.snips.append(snip)

    def _sort_notes(self):
        ''' Keep self.notes sorted descending by the timestamp'''
        notes_sortable = dict()
        for note in self.notes:
            notes_sortable[note.get_timestamp()] = note
        self.notes.clear()
        for note in sorted(notes_sortable.values(), reverse=True):
            self.notes.append(note)

# One and only instance of this class
monoa_service = MonoaService()
