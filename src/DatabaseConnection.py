import sqlite3


class DatabaseConnection:
    connection = None

    @classmethod
    def get_connection(self, db_path):
        if self.connection is None:
            self.connection = sqlite3.connect(db_path)
        return self.connection
