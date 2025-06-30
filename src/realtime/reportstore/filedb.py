import os
import logging
import json
from logging import INFO
from typing import Any
from typing import List, Optional, Union, TYPE_CHECKING
from backend.rtmt import RTMiddleTier, Tool, ToolResult, ToolResultDirection

class FileDBStore:
    logging.basicConfig(level=logging.INFO)

    categories = []

    def load_from_file(self, file_path: str):
        with open(file_path, "r") as file:
            return json.load(file)

    def init_data(self):
        self.logger.info("Creating container in database")
        templates_path = os.path.join(os.path.dirname(__file__), 'categories.json')
        self.categories = self.load_from_file(templates_path)
        # print(self.categories)

    def __init__(self):
        self.logger = logging.getLogger("filedb")
        self.logger.info("Initializing FileDBStore")
        self.init_data()  
    
    async def show_product_information(self, args: Any) -> ToolResult:
        print("showing information")
        information = {
            "title": args["title"],
            "text": args["text"],
            "image": args["image"]
        }
        # Return the result to the client
        return ToolResult(information, ToolResultDirection.TO_CLIENT)
    
    async def show_product_categories(self, args: Any) -> ToolResult:
        print("showing product categories")

        product_categories = []

        for item in self.categories:
            option = {}
            option["title"] = item["title"]
            option["text"] = item["text"]
            option["image"] = item["image"]
            product_categories.append(option)

        # Return the result to the client
        return ToolResult(product_categories, ToolResultDirection.TO_CLIENT)
    
    async def show_product_models(self, args: Any) -> ToolResult:
        print("showing product models for ", args)

        product_models = []

        for item in self.categories:
            if ("variations" in item):
                for varation in item["variations"]:
                    if ("products" in varation):
                        # print(varation)
                        for product in varation["products"]:
                            print(product)
                            option = {}
                            option["title"] = product["title"]
                            option["text"] = product["text"]
                            option["image"] = product["image"]
                            product_models.append(option)  
        
        # Return the result to the client
        return ToolResult(product_models, ToolResultDirection.TO_CLIENT)
    
    async def get_available_categories(self, args: Any) -> ToolResult:
        print("retreiving available categories", args)

        responses = []
        try:
            for item in self.categories:
                option = {}
                option["category_description"] = item["description"]
                option["image"] = item["image"]
                option["text"] = item["text"]
                option["category_name"] = item["category"]
                option["question"] = item["question"]
                responses.append(option)
        except Exception as e:
            print(e)
            return ToolResult("Error", ToolResultDirection.TO_SERVER)
        
        return ToolResult(responses, ToolResultDirection.TO_SERVER)

    async def get_product_variants_by_category(self, args: Any) -> ToolResult:
        category = args["category"].lower()
        print("retreiving category: ", category)

        responses = []

        variants = [
            {
                "id": "1",
                "name": "Combi-steam",
                "category": "Oven",
                "image": "https://media.miele.com/images/2000016/200001600/20000160041.png",
                "text": "Master culinary perfection with the combi steam oven: where moisture meets mastery!",
                "description": "A combi steam oven is a versatile kitchen appliance that combines the functions of a convection oven with steam cooking. It is particularly good for a variety of cooking tasks due to its ability to maintain moisture and enhance flavors. The steam function is excellent for baking bread with a perfect crust, cooking meats that are juicy and tender, and steaming vegetables to preserve nutrients and color. The convection feature allows for even cooking and browning, making it suitable for roasting and baking. This combination of steam and convection makes combi steam ovens ideal for achieving professional-quality results at home across a wide range of dishes."
            },
            {
                "id": "2",
                "name": "Convection",
                "category": "Oven",
                "image": "https://media.miele.com/images/2000017/200001787/20000178722.png",
                "text": "Unlock culinary excellence: Steam and convection in perfect harmony!",
                "description": "A convection steam oven is a versatile appliance that combines convection heating with steam cooking to enhance culinary results. It is particularly good for baking, roasting, and reheating, as the steam helps maintain moisture, ensuring foods like bread have a crisp crust and tender interior, and meats remain juicy. The convection feature ensures even heat distribution, promoting uniform cooking and browning. This combination makes the oven ideal for a variety of tasks, from baking pastries and roasting vegetables to steaming fish and reheating leftovers without drying them out."
            },
            {
                "id": "3",
                "name": "Speed",
                "category": "Oven",
                "image": "https://media.miele.com/images/2000017/200001772/20000177279.png",
                "text": "Fast, flavorful, and fresh: Speed steam oven magic!",
                "description": "A speed steam oven is designed to cook food quickly while preserving moisture and enhancing flavors. It combines the benefits of steam cooking with rapid heating technologies, such as microwave or convection, to significantly reduce cooking times. This makes it ideal for preparing meals efficiently without sacrificing quality. It's particularly useful for busy kitchens, allowing for quick preparation of dishes like steamed vegetables, reheated leftovers, and baked goods, all while maintaining optimal texture and taste. The speed steam oven is perfect for those who need to prepare meals in a hurry but still want the benefits of steam cooking."
            },
            {
                "id": "4",
                "name": "Microwave",
                "category": "Oven",
                "image": "https://media.miele.com/images/2000015/200001542/20000154273.png",
                "text": "Quick & convenient: Microwave your way to mealtime magic!",
                "description": "A microwave is an efficient kitchen appliance known for its ability to quickly heat and cook food using microwave radiation. It is particularly good for reheating leftovers, defrosting frozen items, and cooking simple meals or snacks. Microwaves are also useful for tasks like boiling water, melting butter or chocolate, and steaming vegetables. Their speed and convenience make them ideal for busy households, providing a fast way to prepare food without the need for extensive cooking skills or time.",
            }
        ]

        # for item in self.categories:
        #     if (item["category"].lower() != category.lower().strip()):
        #         continue

        #     for varation in item["variations"]:
        #         try:
      
        #             option = {}
        #             option["name"] = varation["name"]
        #             option["description"] = varation["description"]
        #             option["image"] = varation["image"]
        #             option["text"] = varation["text"]
        #             option["category"] = item["category"]
        #             responses.append(option)
        #         except Exception as e:
        #             print(e)
        #             continue

        return ToolResult(variants, ToolResultDirection.TO_SERVER)
            
    async def get_product_models_by_variant(self, args: Any) -> ToolResult:
        # variant = args["variant"].lower().strip()
        print("retreiving variants: ", args)

        responses = [
                    {
                        "id": "1",
                        "title": "H 7240 BM",
                        "text": "with a seamless design, automatic programmes and combination modes. Available in Stainless steel. Has Touch display with movement sensor.",
                        "image": "https://media.miele.com/images/2000015/200001502/20000150258.png",
                    },
                    {
                        "id": "2",
                        "title": "H 7640 BM",
                        "text": "with a seamless design, automatic programmes and food probe. Available in Stainless steel and glass with. Has Clear text display with sensor controls",
                        "image": "https://media.miele.com/images/2000015/200001502/20000150258.png",
                    }
                ]



        # for item in self.categories:
        #     if (item["category"].lower() != "oven"):
        #         continue
        #     for varation in item["variations"]:
        #         try:
        
        #             if (varation["name"] == "Microwave"):
                        
        #                 for product in varation["products"]:
                           
        #                     option = {}
        #                     option["name"] = product["title"]
        #                     option["description"] = product["description"]
        #                     option["image"] = product["image"]
        #                     option["text"] = product["text"]
        #                     option["category"] = item["category"]
        #                     responses.append(option)
        #         except Exception as e:
        #             print(e)
        #             continue

        return ToolResult(responses, ToolResultDirection.TO_SERVER)
