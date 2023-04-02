import ast

from pathlib import Path

class File(Path):
    def __init__(self, path):
        super().__init__(path)
        # self.name = self.stem
        self.extension = self.suffix
        self.path = self.parent
        self.full_path = self.absolute()

        if self.extension == ".py":
            self.type = "python"

    def barecode(self):
        cleanText = ""
        with open(self.full_path, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    cleanText = cleanText + "\n"
            return cleanText

    def get_meta(self, template):
        if self.extension == ".py":
            return True
        else:
            return None
