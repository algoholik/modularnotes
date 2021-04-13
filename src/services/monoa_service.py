from entities.snippet import Snippet
from entities.note import Note
import database.db_handler as db_handler

class MonoaService:
    def __init__(self):
        self.snippets = []
        for item in db_handler.load_snippets():
            self.snippets.append(Snippet(item['id'], item['snippet'], item['updated']))

    def create_snippet(self, content: str):
        snippet = db_handler.insert_snippet(content)
        self.snippets.append(Snippet(snippet[0], snippet[1], snippet[2]))

    def update_snippet(self, id: int, content: str):
        snippet = db_handler.update_snippet(id, content)

    def get_snippets(self):
        for item in self.snippets:
            yield item

m_service = MonoaService()

