import openai
import os
import json
import glob
import configparser

class HeaderGenerator:
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = self.config.get("openai", "api_key")
        self.project_folder = self.config.get("project", "folder_path")
        self.analysis_file_extension = self.config.get("project", "analysis_file_extension")
        self.template_file = self.config.get("project", "template_file")
        openai.api_key = self.api_key
        self.template = self._read_template()

    def _read_template(self):
        with open(self.template_file, "r") as f:
            return json.load(f)

    def generate_header(self, prompt):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                stop=["\\n"],
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response.choices[0].text
        except Exception as e:
            print("Error: Could not generate header.")
            print(e)
            return None

    def process_files(self):
        analysis_files = glob.glob(f"{self.project_folder}/**/*{self.analysis_file_extension}", recursive=True)

        for file in analysis_files:
            try:
                with open(file, "r") as f:
                    code = f.read()
            except IOError:
                print(f"Error: Could not read code file: {file}")
                continue

            if len(code) > 2000:
                continue

            prompt = self.template["prompt"].format(code=code, filename=os.path.basename(file))
            header = self.generate_header(prompt)

            if header:
                header_postfix = self.template.get("header_postfix", "_header.txt")
                header_filename = f"{os.path.splitext(file)[0]}{header_postfix}"
                try:
                    with open(header_filename, "w") as f:
                        f.write(header)
                except IOError:
                    print(f"Error: Could not write header file: {header_filename}")

    def generate_readme(self, output_file="README.md"):
        header_files = glob.glob(f"{self.project_folder}/**/*_header.txt", recursive=True)
        readme_content = []

        for file in header_files:
            try:
                with open(file, "r") as f:
                    content = f.read()
            except IOError:
                print(f"Error: Could not read header file: {file}")
                continue

            readme_content.append(content)

        readme_text = "\n\n".join(readme_content)
        prompt = self.template["readme_prompt"].format(headers=readme_text)
        readme_generated = self.generate_header(prompt)

        if readme_generated:
            try:
                with open(output_file, "w") as f:
                    f.write(readme_generated)
            except IOError:
                print(f"Error: Could not write README file: {output_file}")