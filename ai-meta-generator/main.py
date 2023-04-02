import os


try:
    from .workspace import WorkspaceCreator
    from .configure import Configuration
    from .chatconnector import OpenAIConnector
    from .template import Template
    from .logger import setup_logger

except ImportError:
    from workspace import WorkspaceCreator
    from configure import Configuration
    from chatconnector import OpenAIConnector
    from template import Template
    from logger import setup_logger


#   what we are doing is we're building a recursive chained query system.

#   said system can generate more data, for which a bot is then created.
#   - steps:
#     - create a workspace
#     - understand data and start knowledge base
    
#     user should be able to:
#         restart bot service with new knowledge base data.
#         start knowledge base gathering tool (ai-meta-generator start or amg start)
#         check intermediate data from source code and modify accordingly
#         create readme file from started knowledge base
#         re-generate intermediate data at will, iteratively
        
    # run bot at will to re-generated context

    # actualy bot can be in a server service.
import logging
# Set up the logger
setup_logger()

logger = logging.getLogger(__name__)

class ExecuteClass:
    def __init__(self, args):
        self.args = args
        self.config = args.config
        self.workspace = None

    def _read_config(self):
        print(self.args.config)
        self.config = Configuration(self.args.config)

    def init(self):
        self.workspace = WorkspaceCreator(config=Configuration(self.config))
        if not self.config:
            self.workspace.create(os.getcwd())
        self._read_config()

    def run(self):
        self.init()
        self.workspace.read()  
        self.process()

    def process(self):
        try:
            logger.info("Processing templates...")
            logger.info("Command Line Args:" + str(self.args))
            
            # Create an OpenAIConnector instance
            connector = OpenAIConnector(self.config)
            
            if self.args.meta:
                
                if self.args.meta == "init":
                    self.init()
                if self.args.meta == "delete":
                    self.workspace.delete_template_results()
                if self.args.meta == "refresh":
                    self.workspace.read()
                    for template in [temp for temp in self.workspace.templates if not temp.hasRan()]:
                        response = template.query(connector, file=self.args.file)
                        print(response)
                        # template.save(response)
                if self.args.meta == "runall":
                    for file in template.files:
                        response = template.query(connector, file)
                        # template.save(response)


            # If a speficic template is specified, process it
            if self.args.template:
                t = Template(self.args.template, self.config)
                
                if self.args.file:
                    t.query(connector, file=self.args.file)
                else:
                    t.query(connector)
            else:
                for template in self.workspace.templates:
                    pass
                    # Process the templates

        except Exception as e:
            print("Error occurred while reading template file: ", e)
            exit(1)

    def delete(self):
        for template in self.workspace.templates:
            template.delete_results()