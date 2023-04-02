# template.py
import json
from pathlib import Path
import os
try:
    from .chatconnector import OpenAIConnector
    from .misc  import read_excludes
except ImportError:
    from chatconnector import OpenAIConnector
    from misc  import read_excludes

# from file import File
import fnmatch
from tqdm import tqdm
import glob

from logging import getLogger
logging = getLogger(__name__)

MODEL_TEMPLATES = {
    "text-davinci-003": {
                "model":"text-davinci-003",
                "max_tokens":2048,
                "stop":["\\n"],
                "temperature":0.7,
                "top_p":1,
                "frequency_penalty":0,
                "presence_penalty":0
            },
    "turbo": {
                "model":"gpt-3.5-turbo",
                "max_tokens":2048,
                "stop":["\\n"],
                "temperature":0.7,
                "top_p":1,
                "frequency_penalty":0,
                "presence_penalty":0
            },
    },


class Template:
    def __init__(self, template_file, config):
        self.config = config
        self.template_file = template_file
        self.path_template = Path(template_file)
        if not self.validation():
            raise Exception("Invalid template file")
            exit(1)
        try:
            self._read_template()
        except Exception as e:
            raise Exception(f"Invalid template file: {e}")
            exit(1)
        self.TreeRecursive = True

    def validation(self):
        if self.template_file.endswith(".json"):
            return True

    def resultsExist(self, sourceCode):
        return Path(self.resultPath(sourceCode)).exists()

    def resultPath(self, sourceCode):
        header_filename = f"{os.path.splitext(sourceCode)[0]}{self.header_postfix}"
        return Path(header_filename)

    def _read_template(self, file=None):
        """_summary_

        Returns:
            _type_: _description_
        """
        if file:
            self.template_file = file  
            self.Path = Path(file) 

        with open(self.template_file, "r") as f:
            template = json.load(f)

            version = template.get("version", "0.0")    

            self.model = template.get("model", "text-davinci-003")
            self.header_postfix = template.get("header_postfix", "_generic.meta")

            self.Chain = template.get("Chain", None)

            if version == "0.0":
                self.analysis_file_extension = template.get("analysis_file_extension")
                if json_structure := template.get("json_structure"):
                    json_structure_str = json.dumps(json_structure, indent=2)
                    template["prompt"] = template["prompt"].replace("$json", json_structure_str)
                self.template = template
            elif version == "0.1":
                self.hasRan = template.get("hasRan", False)
                self.analysis_file_extension = template.get("analysis_file_extension")
                if json_structure := template.get("json_structure"):
                    json_structure_str = json.dumps(json_structure, indent=2)
                    template["prompt"] = template["prompt"].replace("$json", json_structure_str)
                
                self.TreeRecursive = template.get("TreeRecursive", True)
                self.template = template
    
    def isFileRecursive(self):
        return self.TreeRecursive

    def _skip_file(self, file):
        """_summary_

        Args:
            file (_type_): _description_

        Returns:
            _type_: _description_
        """        
        # Skip excluded directories
        # TODO: Handle skipping files in a more graceful way
        skip = False
        for pattern in self.exclude_dirs:
            if any(fnmatch.fnmatch(part, pattern) for part in Path(file).resolve().relative_to(self.config.project_folder).parts for pattern in self.exclude_dirs):
                skip = True
            if pattern in file:
                skip = True
        return skip


    def delete_response(self):
        logging.info(f"Deleting response files for {__name__} {self.path_template.stem}")
        try:
            self.calculatefiles()
        except Exception as e:
            logging.warning(f"Could not calculate files for {self.path_template.stem}. This is likely due to a missing `analysis_file_extension` in the template file.")
            return            
        for file in self.analysis_files:
            if self.resultsExist(file):
                try:
                    logging.info(f"Deleting {self.resultPath(file)}")
                    os.remove(self.resultPath(file))
                except Exception as e:  
                    logging.error(e)
                    pass

    def set_response_callbackprompt(self, callback):
        pass

    def calculatefiles(self):
        logging.info(f"Calculating files for {__name__} {self.path_template.stem}")
        extensions = self.analysis_file_extension
        
        if isinstance(extensions, str):
            extensions = [extensions]
        elif isinstance(extensions, list):
            pass # all good here
        else:
            raise Exception("Invalid analysis_file_extension in template file")
            logging.error("Invalid analysis_file_extension in template file")
        self.analysis_files = []

        for ext in extensions:

            self.analysis_files.extend(glob.glob(f"{self.config.project_folder}/**/*{ext}", recursive=True))
        
        (self.exclude_files_exc, self.exclude_dirs) = read_excludes(".", self.config)
        
        # exclude files
        self.analysis_files = [file for file in self.analysis_files if not any(fnmatch.fnmatch(file, pattern) for pattern in self.exclude_files_exc)]
        
        # skip/exclude files in excluded folder
        self.analysis_files = [file for file in self.analysis_files if not self._skip_file(file)]
        
        return self.analysis_files

    


