import os
import logging
import json
from logging import INFO
from typing import Any
from typing import List, Optional, Union, TYPE_CHECKING

class ReportStore:

    logging.basicConfig(level=logging.INFO)

    templates = []

    def load_from_file(self, file_path: str):
        with open(file_path, "r") as file:
            return json.load(file)


    def __init__(self):
        self.logger = logging.getLogger("reportstore")
        self.logger.info("Initializing ReportStore")
        templates_path = os.path.join(os.path.dirname(__file__), 'templates.json')
        self.templates = self.load_from_file(templates_path)
 
    
    async def get_schema(self, experiment): 
        self.logger.info("Getting report from database")
        try:
            for item in self.templates:
                return item
        except Exception as e:
            self.logger.error(f"Error retrieving schema: {e}")
            return None    
