from .base import BaseHandler, permissions
from tornado.web import authenticated
from tornado import gen


class CreatePost(BaseHandler):
    @permissions(['create_post'])
    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        yield self.render('createpost.html')

    @permissions(['create_post'])
    @authenticated
    @gen.coroutine
    def post(self):
        title = self.get_argument('title')
        if title == '':
            self.error(500, 'Title is required.')
            return
        body = self.get_argument('body')
        if body == '':
            self.error(500, 'Body is required.')
            return
        pinned = self.get_argument('pinned', False)
        uid = self.get_current_user_id()
        post_id = yield self.db.post.create(title, body, uid, pinned)
        self.finish('Created post: %s' % str(post_id))


class DeletePost(BaseHandler):
    @permissions(['create_post'])
    @authenticated
    @gen.coroutine
    def post(self):
        post_id = self.get_argument('post-id')
        yield self.db.post.delete(post_id)
