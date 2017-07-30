from .query import Query
from tornado import gen


class Permission:
    def __init__(self, permissions: dict):
        if type(permissions) != dict:
            permissions = {}
        self.create_post = permissions.get('create_post', False)
        self.create_user = permissions.get('create_user', False)
        self.create_group = permissions.get('create_group', False)
        self.ts3_panel = permissions.get('ts3_panel', False)
        self.csgo_panel = permissions.get('csgo_panel', False)

    def __iter__(self):
        return self.__dict__.__iter__()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()


class PermissionQuery(Query):
    @gen.coroutine
    def get(self, user_id):
        cursor = yield self.execute("""
            SELECT
                p.user_id AS user_id,
                bool_or(g.create_post) AS create_post,
                bool_or(g.create_user) AS create_user,
                bool_or(g.create_group) AS create_group,
                bool_or(g.ts3_panel) AS ts3_panel,
                bool_or(g.csgo_panel) AS csgo_panel
            FROM
                ugc.permissions p
            JOIN
                ugc.user_groups g
            ON
                p.group_name = g.group_name
            WHERE
                user_id = %s
            GROUP BY user_id
            """, [user_id])
        result = cursor.fetchone()
        p = self.parse_result(result, cursor.description)
        return Permission(p)
