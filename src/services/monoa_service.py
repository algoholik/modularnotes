from entities.snippet import Snippet
from entities.note import Note
import database.db_handler as db_handler

# Set the default content for a new snippet
default_snippet_content = ""

# Class for providing up-to-date list of content wherever needed
class MonoaService:
    def __init__(self):
        self.snippets = []
        self.load_snippets()

        # Initialize with an empty snippet if database empty
        if len(self.snippets) == 0:
            snippet = db_handler.create_snippet(default_snippet_content)
            self.snippets.append(Snippet(snippet[0], snippet[1], snippet[2]))

    def load_snippets(self):
        self.snippets.clear()
        for item in db_handler.load_snippets():
            self.snippets.append(Snippet(item['id'], item['snippet'], item['updated']))

    def create_snippet(self, content: str):
        snippet = db_handler.create_snippet(content)
        self.snippets.append(Snippet(snippet[0], snippet[1], snippet[2]))

    def update_snippet(self, id: int, content: str):
        if db_handler.update_snippet(id, content):
            self.load_snippets()
        else:
            print("Could not save to database!")

    def get_snippets(self):
        return self.snippets
    
    def get_snippet(self, id: int):
        result = None
        for snippet in self.snippets:
            if snippet.get_id() == id:
                result = snippet
        return result


# Init MonoaService for global access
m_service = MonoaService()

