import os
import json

class Configuration:

    def __init__(self, path_file="configuration.json"):
        self.configuration_file_path = path_file
        self.__configuration = None
        list_dir = os.listdir()
        if self.configuration_file_path not in list_dir:
            print(os.listdir())
            conf_file = open(self.configuration_file_path, "w")
            conf_file.write("")
            conf_file.close()
            print(os.listdir())

    def __load_configuration(self):
        print(os.listdir())
        conf_file = open(self.configuration_file_path, "r")
        file_str = conf_file.read()
        if file_str == "":
            file_str = "{}"
        self.__configuration = json.loads(file_str)
        conf_file.close()
        return True

    def __save_configuration(self):
        if self.__configuration is not None:
            conf_file = open(self.configuration_file_path, "w")
            conf_file.write(json.dumps(self.__configuration))
            conf_file.close()
            return True
        return False

    def get_settings(self, category="general", name=""):
        if self.__load_configuration():
            if category in self.__configuration.keys():
                if name in self.__configuration[category].keys():
                    return self.__configuration[category][name]
        return None

    def set_settings(self, value, name, category="general"):
        self.__load_configuration()
        s = {}
        if category in self.__configuration.keys():
            s = self.__configuration[category]
        s[name] = value
        self.__configuration[category] = s
        return self.__save_configuration()
