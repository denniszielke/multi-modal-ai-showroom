import json
from enum import Enum
from typing import Any, Callable
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential

class ToolResultDirection(Enum):
    TO_SERVER = 1
    TO_CLIENT = 2

class ToolResult:
    text: str
    destination: ToolResultDirection

    def __init__(self, text: str, destination: ToolResultDirection):
        self.text = text
        self.destination = destination

    def to_text(self) -> str:
        if self.text is None:
            return ""
        return self.text if type(self.text) == str else json.dumps(self.text)

class Tool:
    target: Callable[..., ToolResult]
    schema: Any

    def __init__(self, target: Any, schema: Any):
        self.target = target
        self.schema = schema

class RTToolCall:
    tool_call_id: str
    previous_id: str

    def __init__(self, tool_call_id: str, previous_id: str):
        self.tool_call_id = tool_call_id
        self.previous_id = previous_id


_get_available_locations_tool_schema = {
    "type": "function",
    "name": "get_available_locations",
    "description": "Search the location database for possible car pickup locations. The knowledge base is in English, translate to and from English if " + \
                   "needed. Results are returned in JSON format with a set of metadata that might help the user understand the available options with location, distance and opening hours",
    "parameters": {
        "type": "object",
        "properties": {
            "prefered_location": {
                "type": "string",
                "description": "The user prefered pickup location."
            }
        },
        "required": ["prefered_location"],
        "additionalProperties": False
    }
}

_show_final_details_tool_schema = {
    "type": "function",
    "name": "show_final_details",
    "description": "Shows the user the final details of the car rental including pickup location, car model, pickup and return date.",
    "parameters": {
        "type": "object",
        "properties": {
            "pickup_location": {
                "type": "string",
                "description": "The pickup location selected by the user."
            },
            "car_model": {
                "type": "string",
                "description": "The car model selected by the user."
            },
            "pickup_date": {
                "type": "string",
                "description": "The pickup date selected by the user."
            },
            "return_date": {
                "type": "string",
                "description": "The return date selected by the user."
            }
        },
        "required": ["pickup_location", "car_model", "pickup_date", "return_date"],
        "additionalProperties": False
    }
}

_get_available_models_tool_schema = {
    "type": "function",
    "name": "get_available_cars",
    "description": "Search the model database for possible car models. The knowledge base is in German, translate to and from German if " + \
                   "needed. Results are returned in JSON format with a set of metadata that might help the user understand the available options with name, image, price and available seats.",
    "parameters": {
        "type": "object",
        "properties": {
            "prefered_location": {
                "type": "string",
                "description": "The user prefered pickup location."
            }
        },
        "required": ["prefered_location"],
        "additionalProperties": False
    }
}

_get_available_categories_tool_schema = {
    "type": "function",
    "name": "get_available_categories",
    "description": "Search the product database for available product categories that are available. The knowledge base is in English, translate to and from English if " + \
                   "needed. Results are returned in JSON format with a set of metadata that might help the user understand the available options with title, description and image.",
    "parameters": {
        "type": "object",
        "properties": {
            "input": {
                "type": "string",
                "description": "Some context the provided."
            }
        },
        "required": [],
        "additionalProperties": False
    }
}

_get_product_variants_by_category_tool_schema = {
    "type": "function",
    "name": "get_product_variants_by_category",
    "description": "Search the product database for a set of product variants in a specified category. The knowledge base is in English, translate to and from English if " + \
                   "needed. Results are returned in JSON format with a set of product names, description and image each.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "The name of the product category."
            }
        },
        "required": ["category"],
        "additionalProperties": False
    }
}

_get_product_models_by_variant_schema = {
    "type": "function",
    "name": "get_product_models_by_variant",
    "description": "Search the product database for a set of products of a specific variant. The knowledge base is in English, translate to and from English if " + \
                   "needed. Results are returned in JSON format with a set of product names, description and image each.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "The name of the product variant."
            }
        },
        "required": ["variant"],
        "additionalProperties": False
    }
}

_get_products_tool_schema = {
    "type": "function",
    "name": "get_products",
    "description": "Search the product database for available product variations that the user might be interestd in. The knowledge base is in English, translate to and from English if " + \
                   "needed. Results are returned in JSON format with a set of questions that need to be answered by the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "keywords": {
                "type": "string",
                "description": "keywords that the user has provided to search for product variations."
            }
        },
        "required": ["keywords"],
        "additionalProperties": False
    }
}

_show_product_information_tool_schema = {
    "type": "function",
    "name": "show_product_information",
    "description": "Shows the user a piece of information to support the conversation. The information should be a title, supporting text and reference to an image a that can be displayed to the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the information."
            },
            "text": {
                "type": "string",
                "description": "Additional context that should be displayed to the user."
            },
            "image": {
                "type": "string",
                "description": "The url of the image that should be displayed to the user."
            }
        },
        "required": ["title", "text", "image"],
        "additionalProperties": False
    }
}

_show_product_categories_tool_schema = {
    "type": "function",
    "name": "show_product_categories",
    "description": "Shows the user a piece of information to support the conversation. The information should be a title, supporting text and reference to an image a that can be displayed to the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "product_categories": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category_name": {
                            "type": "string",
                            "description": "The name of the category."
                        },
                        "category_description": {
                            "type": "string",
                            "description": "The description of the category."
                        },
                        "image": {
                            "type": "string",
                            "description": "The url of the image that should be displayed to the user."
                        }
                    },
                    "required": ["category_name", "category_description", "image"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["product_categories"],
        "additionalProperties": False
    }
}

_show_product_models_tool_schema = {
    "type": "function",
    "name": "show_product_models",
    "description": "Shows the user different products information to support the conversation. The information should be a title, supporting text and reference to an image a that can be displayed to the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "product_models": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category_name": {
                            "type": "string",
                            "description": "The name of the category."
                        },
                        "category_description": {
                            "type": "string",
                            "description": "The description of the category."
                        },
                        "image": {
                            "type": "string",
                            "description": "The url of the image that should be displayed to the user."
                        }
                    },
                    "required": ["category_name", "category_description", "image"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["product_models"],
        "additionalProperties": False
    }
}
