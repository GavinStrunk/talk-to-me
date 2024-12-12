from openai import OpenAI

class LlmInterface:
    def send_request(self,
                     request: str
                     ) -> str:
        return ""


class ChatGPT(LlmInterface):
    """
    ChatGPT implementation of the LLM Interface.

    Step 1: OpenAI account and setup API key as describe in [1]
    Step 2: Set up key in environment variable like OPENAI_API_KEY
    Step 2: Must have openai installed

    References:
        [1] https://www.newhorizons.com/resources/blog/chatgpt-api-python-guide
        [2] https://github.com/openai/openai-python
    """
    def __init__(self,
                 api_key: str,
                 model_version: str = "gpt-3.5-turbo",
                 ) -> None:
        self.api_key = api_key
        self.model_version = model_version
        self.client = OpenAI(api_key=api_key)

    def send_request(self,
                     request: str
                     ) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_version,
            messages=[
                {
                    "role": "user",
                    "content": request
                }
            ]
        )
        print(completion)
        return completion.choices[0].text

class Llama(LlmInterface):
    """
    Llama implementation of the LLM Interface.

    Must have Llama model running locally
    """
    def __init__(self,
                 model_version: str
                 ) -> None:
        self.model_version = model_version




if __name__ == '__main__':
    import os
    api_key = os.environ.get('OPENAI_API_KEY')
    llm = ChatGPT(api_key=api_key)
    request = "Did you receive this message?"

    llm.send_request(request)
