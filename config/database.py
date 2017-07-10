from .config import BaseConfig, Entry


class DBConfig(BaseConfig):
    def __init__(self):
        is_str = lambda x: type(x) == str
        skeleton = {'database': Entry('sss', is_str),
                    'username': Entry('postgres', is_str),
                    'password': Entry('', is_str),
                    'hostname': Entry('localhost', is_str),
                    'port': Entry('5432', lambda x: is_str(x) or type(x) == int),
                    'size': Entry(1, lambda x: type(x) == int),
                    'max_size': Entry(None, lambda x: x is None or type(x) == int),
                    'auto_shrink': Entry(False, lambda x: type(x) == bool)}
        super().__init__(skeleton, 'database')

    @property
    def username(self) -> str:
        """
        Username to use when connecting to postgres
        :rtype: str
        :return: postgres username
        """
        return self.raw_config['username']

    @property
    def password(self) -> str:
        """
        Postgres users password
        :rtype: str
        :return: postgres user's password
        """
        return self.raw_config['password']

    @property
    def database(self) -> str:
        """
        Postgres database to connect to
        :rtype: str
        :return: Postgres database name
        """
        return self.raw_config['database']

    @property
    def hostname(self) -> str:
        """
        Hostname of the postgres server
        :rtype: str
        :return: hostname or ip
        """
        return self.raw_config['hostname']

    @property
    def port(self) -> str:
        """
        Port the postgres server is listening on
        :rtype: str
        :return: server port
        """
        return str(self.raw_config['port'])

    @property
    def size(self) -> int:
        """
        Minimum number of database connections to keep open
        :rtype: int
        :return: number of database connections
        """
        return int(self.raw_config['size'])

    @property
    def max_size(self) -> int:
        """
        Maximum number of simultaneous database connections
        :rtype: int
        :return: max number of database connections
        """
        # Set to None if no limit
        return self.raw_config['max_size']

    @property
    def auto_shrink(self) -> bool:
        """
        Automatically garbage collect database connections that have been idle for 120 seconds
        (only applies if max_size is set)
        :rtype: bool
        :return: auto shrink setting
        """
        return self.raw_config['auto_shrink']
