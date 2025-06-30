import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import logging
import json
from logging import INFO
from typing import Any
from typing import List, Optional, Union, TYPE_CHECKING

class FileDBStore:
    logging.basicConfig(level=logging.INFO)

    client: Optional[AzureOpenAI] = None
    categories = []

    def load_from_file(self, file_path: str):
        with open(file_path, "r") as file:
            return json.load(file)

    def init_data(self, endpoint: str, deployment: str, api_version: str):
        self.logger.info("Creating container in database")
        templates_path = os.path.join(os.path.dirname(__file__), 'templates.json')
        self.categories = self.load_from_file(templates_path)
        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
        self.deployment = deployment
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
        )

    def __init__(self):
        self.logger = logging.getLogger("filedb")
        self.logger.info("Initializing FileDBStore")
        self.init_data()  
      
    async def search(self, query:str) -> str:
        print("retreiving available categories", query)

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. What can you do for me on this query with the data below?" + query,
                },
                {
                    "role": "user",
                    "content": self.categories,
                }
            ],
            max_completion_tokens=800,
            temperature=1.0,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            model=self.deployment
        )

        return response.choices[0].message.content