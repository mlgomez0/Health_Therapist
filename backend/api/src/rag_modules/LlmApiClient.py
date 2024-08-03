from colorama import Fore
import requests
import json

class LlmApiClient:
    
    def __init__(self, api_url: str, api_token: str):
        self.phi3_model_url = api_url
        self.azure_api_token = api_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.azure_api_token
        }

    def predict(self, messages):
        """
        Predict the next message based on the conversation history and the user input using an Azure AI endpoint.
        """

        payload = {
            'messages': messages,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "max_tokens": 256,
            "seed": 42,
            "stop": "<|endoftext|>",
            "stream": False,
            "temperature": 0,
            "top_p": 1,
            "response_format": { "type": "text" }
        }

        print(Fore.YELLOW + f"____________________Payload_________________________")
        print(Fore.YELLOW + json.dumps(payload, indent=4))
        print(Fore.WHITE + f"_____________________________________________________")

        response = requests.post(self.phi3_model_url, headers=self.headers, json=payload)
        if response.status_code == 200:

            result = response.json()

            print(Fore.YELLOW + f"____________________Response________________________")
            print("Response:", json.dumps(result, indent=4))
            print(Fore.YELLOW + f"_____________________________________________________")

            model_response = result['choices'][0]['message']['content']
            print("Model's response:", model_response)
            return model_response
        
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return ''

