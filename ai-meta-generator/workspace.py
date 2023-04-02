import os
import shutil
import pkg_resources
import glob
from typing import List
from tqdm import tqdm
try:
    from .misc import generate_tree
    from .template import Template
except ImportError:
    from misc import generate_tree
    from template import Template



class WorkspaceCreator:
    def __init__(self, config):
        self.config = config
        self.project_folder = os.getcwd()
        self.templates = List[Template]
        self.project_tree = {}

    def create(self, root, extra_templates_dir=None):
        # create "templates" directory
        self.path = root
        templates_dir = os.path.join(root, "templates")
        os.makedirs(templates_dir, exist_ok=True)

        # copy packed *.json query templates into "templates" directory
        packed_templates = pkg_resources.resource_listdir(__name__, ".")
        for template in packed_templates:
            if template.endswith(".json"):
                template_path = pkg_resources.resource_filename(__name__, template)
                shutil.copy2(template_path, templates_dir)

        # copy .template.ini into directory
        template_ini_path = pkg_resources.resource_filename(__name__, "../config.sample.ini")
        shutil.copy2(template_ini_path, "./config.ini")

        # save current directory as the root and workspace
        self.project_folder = root

    def delete_template_results(self):
        self.read()
        for template in self.templates: # type: ignore
            template.delete_response()

    def read(self):
        """ _summary_ 
        """        
        
        self.project_tree = generate_tree(self.project_folder, self.config)
        self.templates = []
        for template in os.listdir(os.path.join(self.project_folder,"templates")):
            try:
                if template.endswith(".json") and not template.endswith(".sample.json"):
                    self.templates.append(
                        Template(
                            os.path.join(self.project_folder, "templates", template), 
                            self.config
                        )
                    )
            except Exception as e:
                print("Problem with template: ", template)
                print(e)
        