from os import getenv

import openai
from dotenv import load_dotenv
from openai import ChatCompletion

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint

OPEN_AI__API_KEY = 'OPEN_AI__API_KEY'

class API_Open_AI:

    def __init__(self):
        self.stream = True
        self.temperature = 1.0
        self.model = 'gpt-3.5-turbo' #'gpt-4' #

    @cache_on_self
    def api_key(self):
        load_dotenv()
        return getenv(OPEN_AI__API_KEY)

    def create(self, messages):
        openai.api_key = self.api_key()
        response = ChatCompletion.create(model       = self.model           ,
                                         messages    = messages             ,
                                         temperature = self.temperature     ,
                                         stream      = self.stream          )

        return self.parse_response(response)

    def messages(self):
        return [{"role": "user", "content": 'Hi'}]

    def parse_response(self, response):
        partial_message = ""
        for chunk in response:
            if len(chunk['choices'][0]['delta']) != 0:
                new_content = chunk['choices'][0]['delta']['content']
                yield new_content
                #partial_message = partial_message + new_content
                #yield partial_message

    def setup(self):
        openai.api_key = self.api_key()
        return self

    def ask_one_question_no_history(self,question):
        messages    = [{"role": "user", "content": question}]
        return self.ask_using_messages(messages)

    def ask_using_messages(self, messages):
        response    = self.create(messages)
        full_answer = ""

        for item in response:
            full_answer += item
        return full_answer


    def ask_question_with_user_data_and_prompt(self,user_question, user_data, system_prompt, user_history):
        messages = [{"role": "system", "content": system_prompt},
                    {"role": "system", "content": user_data    }]
        for item in user_history:
            question = item.get('question')
            answer   = item.get('answer')
            messages.append({"role": "user"     , "content": question})
            messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": user_question})

        #pprint(messages)
        return self.ask_using_messages(messages)