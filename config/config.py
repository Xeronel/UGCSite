import yaml
import os


base = os.path.dirname(os.path.dirname(__file__))
file_name = os.path.join(base, 'config.yaml')
with open(file_name, 'r') as f:
    _raw_config = yaml.load(f)


class Entry:
    def __init__(self, value, validate):
        """
        Configuration entry object
        :param value: The default value that should be loaded
        :param validate: Value validation method
        """
        self.value = value
        self.validate = validate


class BaseConfig:
    def __init__(self, skeleton: dict, section: str,):
        """
        Load config.yaml and verify loaded types and load defaults for missing items
        :param skeleton: A dictionary of Entry objects
        :param section: Section of the config file to load
        """
        if section in _raw_config:
            self.raw_config = _raw_config[section]
        else:
            self.raw_config = {section: {}}
        self.__load_config(skeleton)

    def __load_config(self, skeleton: dict):
        """
        :param skeleton: A dictionary of Entry objects
        """
        for k in skeleton:
            if k not in self.raw_config:
                # Load a default value if a the user did not provide one
                self.raw_config[k] = skeleton[k].value
            if not skeleton[k].validate(self.raw_config[k]):
                # Raise an error if the user provided value is not the correct data type
                raise TypeError('Error loading %s' % k)
            if type(skeleton[k]) == dict:
                # Traverse nested dictionaries
                self.__load_config(skeleton[k])
