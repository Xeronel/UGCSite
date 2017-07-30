from .query import Query
from .permission import Permission
from tornado import gen
import psycopg2


class Group:
    def __init__(self, group):
        permissions = {}
        for k, v in group.items():
            if not k == 'group_name':
                permissions[k] = v
        self.name = group['group_name']
        self.permissions = Permission(permissions)


class GroupQuery(Query):
    @gen.coroutine
    def get(self):
        groups = yield self.execute("""
        SELECT
          *
        FROM
          user_groups
        ORDER BY group_name ASC
        """)
        result = self.parse_result(groups.fetchall(), groups.description, cls=Group)
        return result

    @gen.coroutine
    def add_user(self, user_id, group_name):
        try:
            yield self.execute("""
            INSERT INTO
              permissions (user_id, group_name)
            VALUES (%s, %s)
            """, [user_id, group_name])
            return True
        except psycopg2.Error:
            return False
