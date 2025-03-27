

class Library:
    def __init__(self, name: str):
        self.name = name

    def dict(self):
        return {
            'name': self.name
        }
    
    def json(self):
        pass
    