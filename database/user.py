from .query import Query
from .permission import Permission
from tornado import gen
import psycopg2


class User:
    def __init__(self, user: dict, permissions: Permission):
        self.uid = str(user.get('id', -1))
        self.authenticated = False if self.uid == '-1' else True
        self.username = user.get('username', 'Anonymous')
        self.display_name = user.get('display_name', 'Anonymous')
        self.email = user.get('email', 'anonymous@example.com')
        self.permissions = permissions


class UserQuery(Query):
    def __init__(self, db):
        super(UserQuery, self).__init__(db)
        self.permission = db.permission

    @gen.coroutine
    def get(self, user_id: str) -> User:
        """
        Get a users information
        :param user_id: User ID
        :return: User object
        """
        c = yield self.execute("""
        SELECT
            *
        FROM
            users
        WHERE
            id = %s
        """, [user_id])
        u = self.parse_result(c.fetchone(), c.description)
        p = yield self.permission.get(u.get('id', -1))
        return User(u, p)

    @gen.coroutine
    def login(self, username: str, password: str):
        """
        Authenticate a user
        :param username: Username as string
        :param password: Password as string
        :return: User object or False
        """
        try:
            c = yield self.execute("""
            SELECT
              id, username, display_name, email
            FROM
              users
            WHERE
              pwhash = crypt(%s, pwhash)
            AND
              username = %s;
            """, [password, username])
            result = c.fetchone()
            if result is None:
                return False
            else:
                u = self.parse_result(result, c.description)
                p = yield self.permission.get(u.get('id', -1))
                return User(u, p)
        except psycopg2.ProgrammingError:
            return False
