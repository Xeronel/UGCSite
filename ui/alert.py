from tornado import web


class Alert(web.UIModule):
    def render(self):
        return self.render_string('ui/alert.html')
