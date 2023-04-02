import configparser
import os
from logging import getLogger
logging = getLogger(__name__)

class Configuration(configparser.RawConfigParser ):
    def __init__(self, config_file):
        super().__init__()
        self.read(config_file)
        self.api_key = self.get("openai", "api_key")
        if os.path.exists(self.get("project", "folder_path")):
            self.project_folder = self.get("project", "folder_path")
        else:
            logging.error("Project folder does not exist")
            raise Exception("Project folder does not exist")
            
        self.template_file = self.get("project", "template_file")
        self.exclude_dirs = self.get("project", "exclude_dirs").split(",")
