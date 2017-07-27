from .base import BaseHandler
from tornado import gen


class Home(BaseHandler):
    @gen.coroutine
    def get(self):
        posts = yield self.db.post.get()
        yield self.render('index.html', posts=posts)
