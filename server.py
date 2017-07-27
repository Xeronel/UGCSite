from tornado.ioloop import IOLoop as ioloop
from tornado import web
from config import web as config
from database import Database
from handlers import *
import ui


def make_app():
    return web.Application(
        [(r'/', Home),
         (r'/login', Login),
         (r'/logout', Logout),
         (r'/create_user', CreateUser),
         (r'/create_post', CreatePost),
         (r'/delete_post', DeletePost),
         (r'/image_upload', ImageUpload)],
        debug=config.debug,
        autoreload=config.autoreload,
        compiled_template_cache=config.compiled_template_cache,
        static_path=config.static_path,
        template_path=config.template_path,
        login_url='/login',
        cookie_secret=config.cookie_secret,
        key_version=config.key_version,
        xsrf_cookies=True,
        ui_modules=ui)


if __name__ == '__main__':
    # Create a new web application
    app = make_app()
    app.listen(config.port)

    # Attempt to connect to the database
    ioloop = ioloop.current()
    app.database = Database(ioloop)
    future = app.database.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    # Start the app
    ioloop.start()
