from .base import BaseHandler, permissions
from tornado import gen, web
from uuid import uuid4
import os


class ImageUpload(BaseHandler):
    @permissions(['create_post'])
    @web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        self.require_setting('static_path', 'image upload.')

        if self.request.files:
            allowed_types = ['.jpg', '.jpeg', '.png', '.gif']
            for val in self.request.files.values():
                for file in val:
                    try:
                        ext = os.path.splitext(file['filename'])[1]
                        if ext in allowed_types:
                            filename = uuid4().hex + ext
                            path = os.path.join(self.settings.get('static_path'), 'uploads')
                            full_path = os.path.join(path, filename)
                            with open(full_path, 'wb') as f:
                                f.write(file['body'])
                            self.finish(
                                '%s%s%s' % (self.settings.get("static_url_prefix", "/static/"), 'uploads/', filename))
                        else:
                            self.error(500, 'Invalid file type. Allowed types are %s' % ', '.join(allowed_types))
                    except (KeyError, PermissionError, TypeError, FileExistsError, FileExistsError) as e:
                        self.error(500, 'Invalid file data.')
                        if full_path and os.path.isfile(full_path):
                            os.remove(full_path)
        else:
            self.error(500, 'File is missing or cannot be found.')
