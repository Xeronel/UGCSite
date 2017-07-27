from .query import Query
from tornado import gen
from datetime import date, datetime


class Post:
    def __init__(self, post: dict):
        self.id = post['id']
        self.username = str(post['username'])
        self.title = str(post['title'])
        self.body = str(post['body'])
        created_on = post['created_on']
        if type(created_on) == date or type(created_on) == datetime:
            self.created_on = created_on
        else:
            raise TypeError('created_on must be a date')


class PostQuery(Query):
    def __init__(self, db):
        super(PostQuery, self).__init__(db)
        self.permission = db.permission

    @gen.coroutine
    def get(self):
        posts = yield self.execute("""
        SELECT
            u.username, p.title, p.body, p.created_on, p.id
        FROM
            posts p
        LEFT JOIN
            users AS u ON u.id = p.created_by
        ORDER BY pinned DESC, created_on DESC
        LIMIT 10
        """)
        return self.parse_result(posts.fetchall(), posts.description,
                                 convert_date=False, cls=Post)

    @gen.coroutine
    def create(self, title: str, body: str, created_by: int, pinned=False):
        """
        Create a post
        :param title: Post title
        :param body: Post body
        :param created_by: ID of the user creating the post
        :param pinned: Sort this post first
        :return: Post id
        """
        c = yield self.execute("""
        INSERT INTO
            posts (title, body, created_by, pinned)
        VALUES
            (%s, %s, %s, %s)
        RETURNING id;
        """, [title, body, created_by, pinned])
        return c.fetchone()[0]

    @gen.coroutine
    def delete(self, post_id):
        yield self.execute("DELETE FROM posts WHERE id = %s", [post_id])
