class Query:
    def __init__(self, db):
        self.execute = db.execute
        self.parse_result = db.parse_result
        self.pool = db.pool
        self.connect = db.connect
