from .database import DBConfig as __DBConfig
from .web import WebConfig as __WebConfig

db = __DBConfig()
web = __WebConfig()
__all__ = ['db', 'web', 'smtp']
