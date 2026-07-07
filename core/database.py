class Database:

    def __init__(self):
        self.storage = []
        print("Database initialized")

    def save(self, data):
        print("Saving data to database...")

        if not data:
            return

        self.storage.append(data)

    def get_all(self):
        return self.storage