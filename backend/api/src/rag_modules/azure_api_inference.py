import os
import requests


class LlmTalker:
    
    def __init__(self):
        self.azure_api_token = os.getenv("AZURE_API_TOKEN")
        self.phi3_model_url = os.getenv("PHI3_MODEL_URL")
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.azure_api_token
        }
        

    def chat(self, chat_history, context, user_input):

        payload = {
            'messages': chat_history + [
                {
                    'role': 'system',
                    'content': f"Context: {context}"
                },
                {
                    'role': 'user',
                    'content': user_input
                }
            ]
        }

 
        response = requests.post(self.phi3_model_url, headers=self.headers, json=payload)


        if response.status_code == 200:

            result = response.json()

            model_response = result['choices'][0]['message']['content']
            print("Model's response:", model_response)
            return model_response
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return ''
