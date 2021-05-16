'''
Main module for handling notes and snips between UI and DB
- provides up-to-date lists of snips and notes
- keeps the lists sorted by timestamp, latest first
'''
from collections import OrderedDict
from datetime import datetime
from entities.note import Note
from entities.snip import Snip
import database.db_handler as db_handler

class MonoaService:
    ''' Main content handler class.
        - Provides up-to-date data structures containing all notes and snips.
        - Handles communication of note and snip modifications between UI and DB.
        - Provides different ways of getting and updating notes and snips.
    '''
    def __init__(self):
        ''' Load all notes and snip to lists '''
        self.notes = list()
        self.snip_dict = OrderedDict()
        self.note_dict = OrderedDict()
        self._load_notes()
        self._autocreate_note_if_none()

    def create_note(self, title: str) -> Note:
        ''' Create a new note by doing the following:
            1. Creates a new note in database to receive a unique id.
            2. Creates a new snip in database and adds it to the note.
        '''
        init_snip = self.create_snip("")
        snip_list = ";".join([str(init_snip.get_id())])
        note = db_handler.create_note(title, snip_list, datetime.now())
        self.note_dict[note['id']] =    Note(
                                            note['id'],
                                            note['title'],
                                            note['contents'],
                                            note['modified']
                                        )
        self._load_notes()
        return self.get_note_by_id(note['id'])

    def create_snip(self, content: str) -> Snip:
        ''' Create new snip. '''
        snip = db_handler.create_snip(0, content, datetime.now())
        self.snip_dict[snip['id']] =    Snip(
                                            snip['id'],
                                            snip['sniptype'],
                                            snip['content'],
                                            snip['modified']
                                        )
        self._load_snips()
        return self.get_snip_by_id(snip['id'])

    def create_snip_inside_note(self, note_id: int) -> Snip:
        ''' Adds a new snip inside the note currently under editing. '''
        snip = self.create_snip("")
        self.note_dict.get(note_id).add_content(snip)
        self.update_note(self.get_note_by_id(note_id))
        return snip

    def get_note_by_id(self, note_id: int) -> Note:
        ''' Returns note by its id '''
        return self.note_dict.get(note_id)

    def get_snip_by_id(self, note_id: int) -> Snip:
        ''' Returns snip by its id '''
        return self.snip_dict.get(note_id)

    def update_note(self, note: Note) -> None:
        ''' Updates note in database. '''
        contents = []
        for snip in note.get_contents():
            contents.append(str(snip.get_id()))
        db_handler.update_note(
            note.get_id(),
            note.get_title(),
            contents,
            note.get_modified()
        )
        self._load_notes()
        self._sort_notes()

    def get_notes(self) -> list:
        ''' Return all notes as a list of note objects. '''
        if len(self.note_dict) == 0:
            self.create_note("")
            self._load_notes()
        return list(self.note_dict.values())

    def get_snips(self) -> list:
        ''' Return all snips as a list of snip objects. '''
        return list(self.snip_dict.values())

    def get_latest_note_id(self) -> int:
        ''' Return last modified note's id as int. '''
        return max(self.note_dict)

    def get_latest_note(self) -> Note:
        ''' Return last modified note as note object. '''
        note_id = next(reversed(self.note_dict))
        return self.note_dict.get(note_id)

    def _load_notes(self) -> None:
        ''' Load all notes from database. '''
        self._load_snips()
        for note in db_handler.load_notes():
            snips = [self.get_snip_by_id(int(snip)) for snip in note['contents'].split(";")]
            self.note_dict[note['id']] =    Note(
                                                note['id'],
                                                note['title'],
                                                snips,
                                                note['modified']
                                            )

    def _sort_notes_pro(self):
        def sort_by_date(note: Note):
            return note.get_modified()
        return list(reversed(sorted(self.note_dict, key=sort_by_date)))

    def _load_snips(self) -> None:
        ''' Load all snips from database. '''
        for snip in db_handler.load_snips():
            self.snip_dict[snip['id']] =    Snip(
                                                snip['id'],
                                                snip['sniptype'],
                                                snip['content'],
                                                snip['modified']
                                            )

    def _autocreate_note_if_none(self) -> None:
        ''' If database has zero notes, create a placeholder note. '''
        if len(self.note_dict) == 0:
            self.create_note("")

    def _sort_notes(self) -> None:
        ''' Keep self.notes sorted descending by the timestamp'''
        notes_sortable = OrderedDict()
        for key, value in self.note_dict.items():
            notes_sortable[value.get_modified()] = value
        for key, value in sorted(notes_sortable.items(), reverse=True):
            self.note_dict[key] = value

    def _sort_snips(self) -> None:
        ''' Keep self.snips sorted descending by the timestamp'''
        snips_sortable = OrderedDict()
        for key, value in self.snip_dict.items():
            snips_sortable[value.get_modified()] = value
        for key, value in sorted(snips_sortable.items(), reverse=True):
            self.snip_dict[key] = value

    def update_snip(self, snip: Snip) -> None:
        ''' Update snip by the given id '''
        db_handler.update_snip(
            snip.get_id(),
            snip.get_sniptype(),
            snip.get_content(),
            datetime.now()
        )
        self._load_snips()
        self._sort_snips()

    def render_textfile_contents(self, note_id: int) -> str:
        ''' Returns note contents as a string for file exporting. '''
        contents: list = []
        for snip in self.get_note_by_id(note_id).get_contents():
            contents.append(snip.get_content())
        return "\n".join(contents)

# One and only instance of this class
monoa_service = MonoaService()
