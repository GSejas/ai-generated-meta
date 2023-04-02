import logging
import openai



class Connector():

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.debug("Connector init")

    def init(self, **kwargs):
        # Pass the model parameters here
        pass

    def Query(self, prompt, **kwargs):
        # They can use kwargs to modify this particular call
        # Pass the prompt here
        return None

class ResponseLog():
    def __init__(self):
        self.response = []

    def Add(self, prompt, context, response):
        self.response.append({
            "prompt": prompt,
            "context": context,
            "response": response
        })

        
class OpenAIConnector(Connector):
    
    def __init__(self, config, **kwargs):
        
        self.logger = logging.getLogger(__name__)
        self.config = config

        openai.api_key = self.config.api_key

    def init(self, **kwargs):
        # Pass the model parameters here
        pass

    def Query(self, prompt, **kwargs):
        # They can use kwargs to modify this particular call
        # Pass the prompt here
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=2048,
        #     stop=["\\n"],
        #     temperature=0.7,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        # )
        self.logger.debug("OpenAIConnector Query")
        self.logger.debug(prompt)
        response = openai.Completion.create(
            prompt=prompt,
            **kwargs
        )
        return response