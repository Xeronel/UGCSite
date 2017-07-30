from .query import Query
from tornado import gen
from datetime import date, datetime


class Post:
    def __init__(self, post: dict):
        self.id = post['id']
        self.title = str(post['title'])
        self.body = str(post['body'])
        self.created_by = str(post['created_by'])
        self.pinned = bool(post['pinned'])
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
    def get_all(self):
        posts = yield self.execute("""
        SELECT
            u.display_name AS created_by, p.title, p.body, p.created_on, p.pinned, p.id
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
    def get(self, post_id):
        post = yield self.execute("""
        SELECT
            u.display_name AS created_by, p.title, p.body, p.created_on, p.pinned, p.id
        FROM
            posts p
        LEFT JOIN
            users AS u ON u.id = p.created_by
        WHERE p.id = %s
        """, [post_id])
        return self.parse_result(post.fetchone(), post.description,
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
    def update(self, post_id: int, title: str, body: str, created_by: int, pinned=False):
        post = yield self.execute("""
        UPDATE
            posts
        SET
          title = %s, body = %s, created_by = %s, pinned = %s
        WHERE
          id = %s
        RETURNING id
        """, [title, body, created_by, pinned, post_id])
        return post

    @gen.coroutine
    def delete(self, post_id):
        yield self.execute("DELETE FROM posts WHERE id = %s", [post_id])
