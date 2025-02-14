from api.prompt import Prompt
#from prompt import Prompt

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        #self.model = os.getenv("OPENAI_MODEL", default = "text-davinci-003")
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default = 0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default = 0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 90))
    """
    def get_response(self):
        response = openai.Completion.create(
            model=self.model,
            prompt=self.prompt.generate_prompt(),
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            max_tokens=self.max_tokens
        )
        return response['choices'][0]['text'].strip()
    """
    def get_response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
	    temperature=self.temperature,
	    frequency_penalty=self.frequency_penalty,
	    presence_penalty=self.presence_penalty,
	    max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": "系統訊息，目前無用"},
                {"role": "assistant", "content": "此處填入機器人訊息"},
                #{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": self.prompt.generate_prompt()}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    
    def translate_openai(self, text, language):
        prompt = f"""'{text}'
        Help me to translate this sentence to {language}, only target language, no need original language."""

        # Translate the chunk using the GPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # engine = "deployment_name".
            messages= [{"role":"user", "content":prompt}],
            temperature = 0.5
        )
        translated_subtitles = response['choices'][0]['message']['content']
        return translated_subtitles
    
    def add_msg(self, text):
        self.prompt.add_msg(text)
    
    def clear_msg(self):
        self.prompt.clear_msg()
