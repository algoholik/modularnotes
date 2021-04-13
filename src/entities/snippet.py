from datetime import datetime

class Snippet:
    def __init__(self, id: int, snippet: str, updated: datetime):
        self.id = id
        self.snippet = snippet
        self.updated = updated
        
    def get_id(self):
        return self.id

    def get_snippet(self):
        return self.snippet

    def get_updated(self):
        return self.updated

    def __str__(self):
        return f"snippet id: {self.id} (created {self.updated}): {self.snippet}"
