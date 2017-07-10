from .config import BaseConfig, Entry
import os


def _check_cs(value):
    # Allow a single cookie secret as a string
    if type(value) == str:
        return True

    if type(value) == dict:
        for k, v in value.items():
            # Dictionaries of secrets must have numbers set as keys
            if type(k) != int:
                return False
            # All keys must be strings
            if type(v) != str:
                return False
        return True


class WebConfig(BaseConfig):
    def __init__(self):
        base = os.path.dirname(os.path.dirname(__file__))
        is_bool = lambda x: type(x) == bool
        is_str = lambda x: type(x) == str
        skeleton = {'debug': Entry(False, is_bool),
                    'autoreload': Entry(False, is_bool),
                    'compiled_template_cache': Entry(True, is_bool),
                    'static_path': Entry(os.path.join(base, 'static'), is_str),
                    'template_path': Entry(os.path.join(base, 'templates'), is_str),
                    'cookie_secret': Entry({0: 'j9Wy1m*3CnwKw!AFd5sd3kl@'}, _check_cs),
                    'key_version': Entry(0, lambda x: type(x) == int),
                    'port': Entry(8181, lambda x: type(x) == int)}
        super().__init__(skeleton, 'web_server')

        # Set some additional defaults if in debug mode
        if self.debug:
            self.raw_config['compiled_template_cache'] = False
            self.raw_config['autoreload'] = False
        else:
            self.raw_config['compiled_template_cache'] = True
            self.raw_config['autoreload'] = True

        # Make sure cookie_secret is stored as a dictionary
        if type(self.raw_config['cookie_secret']) == str:
            self.raw_config['cookie_secret'] = {0: self.raw_config['cookie_secret']}
            self.raw_config['key_version'] = 0

        if self.key_version not in self.cookie_secret:
            raise ValueError('Invalid key version')

    @property
    def debug(self) -> bool:
        """
        Tornado web application debug setting
        :rtype: bool
        :return: debug mode
        """
        return self.raw_config['debug']

    @property
    def autoreload(self) -> bool:
        """
        Tornado autoreload application setting
        :rtype: bool
        :return: autoreload setting
        """
        return self.raw_config['autoreload']

    @property
    def compiled_template_cache(self) -> str:
        """
        Recompile templates on each page view or cache them
        :rtype: bool
        :return: template cache setting
        """
        return self.raw_config['compiled_template_cache']

    @property
    def static_path(self) -> str:
        """
        The location of static web files
        :rtype: str
        :return: static file directory
        """
        return self.raw_config['static_path']

    @property
    def template_path(self) -> str:
        """
        The location of html template files
        :rtype: str
        :return: template directory
        """
        return self.raw_config['template_path']

    @property
    def cookie_secret(self) -> dict:
        """
        A dictionary of cookie secrets indexed by version number
        :rtype: dict
        :return: cookie secret dictionary
        """
        return self.raw_config['cookie_secret']

    @property
    def key_version(self) -> int:
        """
        Which cookie secret version to use
        :rtype: int
        :return: cookie secret version
        """
        return int(self.raw_config['key_version'])

    @property
    def port(self):
        return int(self.raw_config['port'])
