import psycopg2
import momoko
import config
from tornado import gen
from datetime import date, datetime
from decimal import Decimal
from .permission import PermissionQuery
from .user import UserQuery
from .post import PostQuery
from .group import GroupQuery


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
        self.post = PostQuery(self)
        self.group = GroupQuery(self)

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

    def parse_result(self, data, description, convert_decimal=True, convert_date=True, cls=None):
        if type(data) == list:
            result = []
            for value in data:
                if cls is not None:
                    result.append(self.parse_result(value, description, convert_decimal, convert_date, cls))
                else:
                    result.append(self.parse_result(value, description, convert_decimal, convert_date, cls))
        elif type(data) == tuple:
            result = {}
            for i in range(len(description)):
                if type(data[i]) == date or type(data[i]) == datetime and convert_date:
                    value = data[i].strftime('%Y-%m-%d')
                elif type(data[i]) == Decimal and convert_decimal:
                    value = str(data[i])
                else:
                    value = data[i]
                result[description[i].name] = value
            if cls is not None:
                result = cls(result)
        else:
            result = {}
        return result
