import os
import logging
import json
from logging import INFO
from typing import Any
from typing import List, Optional, Union, TYPE_CHECKING
from backend.rtmt import RTMiddleTier, Tool, ToolResult, ToolResultDirection

class RentalDBStore:
    logging.basicConfig(level=logging.INFO)

    def __init__(self):
        self.logger = logging.getLogger("rentaldb")
        self.logger.info("Initializing rentaldb")
   

    async def show_product_information(self, args: Any) -> ToolResult:
        print("showing information")
        information = {
            "title": args["title"],
            "text": args["text"],
            "image": args["image"]
        }
        # Return the result to the client
        return ToolResult(information, ToolResultDirection.TO_CLIENT)
  


    async def get_available_locations(self, args: Any) -> ToolResult:
        print("retreiving available locations", args)

        responses = [
                {
                    "id": "1",
                    "name": "Düsseldorf Airport",
                    "title": "Düsseldorf Airport",
                    "image": "https://www.dus.com/-/media/dus/businesspartner/aviation/general-aviation/executive_terminal_1920x1080px.ashx",
                    "address": "Flughafenstraße 120, 40474 Düsseldorf, Germany",
                    "distance": "30 km",
                    "opening_hours": "Mo - So 06:00 - 23:30"
                },
                {
                    "id": "2",
                    "name": "Cologne Central Station",
                    "address": "Trankgasse 11, 50667 Köln, Germany",
                    "distance": "25 km",
                    "opening_hours": "Mo - So 05:00 - 22:00"
                },
                {
                    "id": "3",
                    "name": "Frankfurt Main Airport",
                    "address": "60547 Frankfurt am Main, Germany",
                    "distance": "120 km",
                    "opening_hours": "Mo - So 24/7"
                },
                {
                    "id": "4",
                    "name": "Berlin Tegel Airport",
                    "address": "Friedrichstraße 50, 10117 Berlin, Germany",
                    "distance": "650 km",
                    "opening_hours": "Mo - So 24/7"
                },
                {
                    "id": "5",
                    "name": "Munich Central Station",
                    "address": "Bahnhofplatz 1, 80335 München, Germany",
                    "distance": "500 km",
                    "opening_hours": "Mo - So 04:00 - 01:00"
                }
            ]
        
        return ToolResult(responses, ToolResultDirection.TO_SERVER)

    async def get_available_cars(self, args: Any) -> ToolResult:
        print("retreiving available cars", args)

        responses = [
                {
                    "id": "1",
                    "name": "SUV",
                    "title": "SUV",
                    "image": "http://localhost:8765/static/cars/cat_1_var_1.png",
                    "text": "Ein vollelektrischer SUV, der die Zukunft der Mobilität verkörpert.",
                    "description": "Der vollelektrische SUV bietet eine beeindruckende Reichweite von 500 km und ist mit modernster Technologie ausgestattet. Er verfügt über ein geräumiges Interieur, fortschrittliche Sicherheitsfunktionen und ein elegantes Design.",
                    "price": "90.00 € per day",
                    "seats": 6,
                    "transmission": "Automatic",
                },
                {
                    "id": "2",
                    "name": "Sedan",
                    "title": "Practical Sedan",
                    "image": "http://localhost:8765/static/cars/cat_1_var_2_mod_2.png",
                    "text": "Ein luxuriöser Sedan mit fortschrittlicher Technologie.",
                    "description": "Der luxuriöse Sedan bietet eine Kombination aus Komfort und Leistung. Er ist mit einem leistungsstarken Motor ausgestattet, der eine sanfte Fahrt ermöglicht. Das Interieur ist mit hochwertigen Materialien gestaltet und bietet modernste Infotainment-Systeme.",
                    "price": "60.00 € per day",
                    "seats": 5,
                    "transmission": "Automatic",
                },
                {
                    "id": "3",
                    "name": "Compact",
                    "title": "Compact City Car",
                    "image": "http://localhost:8765/static/cars/cat_1_var_3.png",
                    "text": "Ein kompakter und effizienter Stadtwagen.",
                    "description": "Der kompakte Stadtwagen ist ideal für den urbanen Verkehr. Er bietet eine hohe Kraftstoffeffizienz und ist leicht zu parken. Das Interieur ist funktional",
                    "price": "55.00 € per day",
                    "seats": 4,
                    "transmission": "Manual",
                },
                {
                    "id": "4",
                    "name": "Limousine",
                    "title": "Elegant Limousine",
                    "image": "http://localhost:8765/static/cars/cat_1_var_2_mod_1.png",
                    "text": "Eine elegante Limousine für besondere Anlässe.",
                    "description": "Die elegante Limousine bietet Luxus und Stil. Sie ist mit einem leistungsstarken Motor ausgestattet und bietet ein geräumiges Interieur mit hochwertigen Materialien. Ideal für besondere Anlässe oder Geschäftsreisen.",
                    "price": "85.00 € per day",
                    "seats": 5,
                    "transmission": "Automatic",
                }
            ]
        
        return ToolResult(responses, ToolResultDirection.TO_SERVER) 