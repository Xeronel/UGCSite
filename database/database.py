import psycopg2
import momoko
import config
from tornado import gen
from datetime import date, datetime
from decimal import Decimal
from .permission import PermissionQuery
from .user import UserQuery


class Database:
    def __init__(self, ioloop):
        self.pool = momoko.Pool(dsn="dbname=%s user=%s password=%s host=%s port=%s" %
                                    (config.db.database, config.db.username, config.db.password,
                                     config.db.hostname, config.db.port),
                                size=1,
                                max_size=config.db.max_size,
                                auto_shrink=config.db.auto_shrink,
                                ioloop=ioloop)
        self.permission = PermissionQuery(self)
        self.user = UserQuery(self)

    def connect(self):
        return self.pool.connect()

    @gen.coroutine
    def execute(self, *args, **kwargs):
        # Throws momoko.PartiallyConnectedError if database is down
        try:
            cursor = yield self.pool.execute(*args, **kwargs)
        except psycopg2.OperationalError:
            yield self.connect()
            cursor = yield self.pool.execute(*args, **kwargs)
        return cursor

    def parse_result(self, data, description, convert_decimal=True):
        if type(data) == list:
            result = []
            for value in data:
                result.append(self.parse_result(value, description))
        elif type(data) == tuple:
            result = {}
            for i in range(len(description)):
                if type(data[i]) == date or type(data[i]) == datetime:
                    value = data[i].strftime('%Y-%m-%d')
                elif type(data[i]) == Decimal and convert_decimal:
                    value = str(data[i])
                else:
                    value = data[i]
                result[description[i].name] = value
        else:
            result = {}
        return result
