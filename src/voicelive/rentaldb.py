import os
import logging
import json
from logging import INFO
from typing import Any
from typing import List, Optional, Union, TYPE_CHECKING

class RentalDBStore:
    logging.basicConfig(level=logging.INFO)

    def __init__(self):
        self.logger = logging.getLogger("rentaldb")
        self.logger.info("Initializing rentaldb")
   

    async def show_product_information(self, args: Any) -> dict:
        print("showing information")
        information = {
            "title": args["title"],
            "text": args["text"],
            "image": args["image"]
        }
        # Return the result to the client
        return information
  


    async def get_available_locations(self, args: Any) -> List[dict]:
        print("retreiving available locations", args)

        url = "http://localhost:8765/static/locations/"

        responses = [
                {
                    "id": "1",
                    "name": "Düsseldorf Airport",
                    "title": "Düsseldorf Airport",
                    "image": url + "pickup_dus.png",
                    "address": "Flughafenstraße 120, 40474 Düsseldorf, Germany",
                    "distance": "10 km",
                    "opening_hours": "Mo - So 06:00 - 23:30"
                },
                {
                    "id": "2",
                    "name": "Cologne Central Station",
                    "title": "Cologne Central Station",
                    "image": url + "pickup_col.png",
                    "address": "Trankgasse 11, 50667 Köln, Germany",
                    "distance": "25 km",
                    "opening_hours": "Mo - So 05:00 - 22:00"
                },
                {
                    "id": "6",
                    "name": "Cologne Airport",
                    "title": "Cologne Airport",
                    "image": url + "pickup_cgn.png",
                    "address": "Kennedystraße 400, 51147 Köln, Germany",
                    "distance": "30 km",
                    "opening_hours": "Mo - So 06:00 - 23:30"
                },                
                {
                    "id": "3",
                    "name": "Frankfurt Main Airport",
                    "title": "Frankfurt Main Airport",
                    "image": url + "pickup_fra.png",
                    "address": "60547 Frankfurt am Main, Germany",
                    "distance": "120 km",
                    "opening_hours": "Mo - So 24/7"
                },
                {
                    "id": "4",
                    "name": "Berlin Tegel Airport",
                    "title": "Berlin Tegel Airport",
                    "image": url + "pickup_ber.png",
                    "address": "Friedrichstraße 50, 10117 Berlin, Germany",
                    "distance": "650 km",
                    "opening_hours": "Mo - So 24/7"
                },
                {
                    "id": "5",
                    "name": "Munich Central Station",
                    "title": "Munich Central Station",
                    "image": url + "pickup_muc.png",
                    "address": "Bahnhofplatz 1, 80335 München, Germany",
                    "distance": "500 km",
                    "opening_hours": "Mo - So 04:00 - 01:00"
                }

            ]
        
        return responses

    async def get_available_cars(self, args: Any) -> List[dict]:
        print("retreiving available cars", args)

        url = "http://localhost:8765/static/cars/"

        responses = [
               {
                "id": "1",
                "title": "SUV",
                "description": "A spacious electric SUV with a panoramic sunroof, dual-motor all-wheel drive, and advanced driver assistance systems. Ideal for families and long-distance travel.",
                "image": url + "electric_suv.png",
                "image_description": "Modern electric SUV with sleek design and panoramic roof",
                "distance": "580 km",
                "passengers": "5",
                "trunk": "550 l",
                "pricePerDay": "ab 140 €",
                "pricePerWeek": "ab 840 €",
                "features": "Dual motor AWD, 400 kW power, 0-100 km/h in 4.5s, top speed 210 km/h"
            },
            {
                "id": "2",
                "title": "Limousine",
                "description": "A premium electric limousine with luxurious interior, ambient lighting, and a smooth, quiet ride. Perfect for business travel and city cruising.",
                "image": url + "electirc_limousine.png",
                "image_description": "Elegant electric limousine with ambient lighting",
                "distance": "520 km",
                "passengers": "5",
                "trunk": "480 l",
                "pricePerDay": "ab 130 €",
                "pricePerWeek": "ab 780 €",
                "features": "Rear-wheel drive, 300 kW power, 0-100 km/h in 5.8s, top speed 200 km/h"
            },{
                "id": "3",
                "title": "Mini Bus",
                "description": "A compact bus suitable for small groups, featuring comfortable seating and air conditioning.",
                "image": url + "mini_bus.png",
                "image_description": "Mini bus parked near a hotel entrance",
                "distance": "600 km",
                "passengers": "12",
                "trunk": "1000 l",
                "pricePerDay": "ab 200 €",
                "pricePerWeek": "ab 1200 €",
                "features": "Air conditioning, reclining seats, USB charging ports"
            },
            {
                "id": "4",
                "title": "Coach Bus",
                "description": "A full-size coach bus with onboard restroom, entertainment system, and large luggage compartments.",
                "image": url + "coach_bus.png",
                "image_description": "Luxury coach bus on highway",
                "distance": "800 km",
                "passengers": "50",
                "trunk": "3000 l",
                "pricePerDay": "ab 400 €",
                "pricePerWeek": "ab 2400 €",
                "features": "Restroom, Wi-Fi, TV screens, climate control"
            },
            {
                "id": "5",
                "title": "Compact Sedan",
                "description": "A fuel-efficient compact sedan with modern features and comfortable seating for daily commutes.",
                "image": url + "compact_sedan.png",
                "image_description": "Compact petrol sedan in urban environment",
                "distance": "700 km",
                "passengers": "5",
                "trunk": "400 l",
                "pricePerDay": "ab 60 €",
                "pricePerWeek": "ab 360 €",
                "features": "1.6L engine, automatic transmission, cruise control"
            },
            {
                "id": "6",
                "title": "Family SUV",
                "description": "A spacious petrol SUV with high ground clearance and versatile cargo space. Great for family trips.",
                "image": url + "familiy_suv.png",
                "image_description": "Petrol SUV parked near a park",
                "distance": "650 km",
                "passengers": "5",
                "trunk": "600 l",
                "pricePerDay": "ab 90 €",
                "pricePerWeek": "ab 540 €",
                "features": "2.0L engine, all-wheel drive, roof rails"
            },
            {
                "id": "7",
                "title": "Coupe",
                "description": "A high-performance electric coupe with aggressive styling, low center of gravity, and track-ready dynamics.",
                "image": url + "sportscar.png",
                "image_description": "Electric sports coupe on a mountain road",
                "distance": "450 km",
                "passengers": "2",
                "trunk": "200 l",
                "pricePerDay": "ab 180 €",
                "pricePerWeek": "ab 1080 €",
                "features": "500 kW power, 0-100 km/h in 3.2s, top speed 250 km/h, carbon fiber body"
            },
            {
                "id": "8",
                "title": "Roadster",
                "description": "An open-top electric roadster with exhilarating acceleration and a minimalist interior focused on the driving experience.",
                "image": url + "roadster.png",
                "image_description": "Electric roadster with top down on coastal highway",
                "distance": "420 km",
                "passengers": "2",
                "trunk": "150 l",
                "pricePerDay": "ab 190 €",
                "pricePerWeek": "ab 1140 €",
                "features": "480 kW power, 0-100 km/h in 3.5s, top speed 240 km/h, convertible roof"
            },{
                "id": "9",
                "title": "Executive Sedan",
                "description": "A refined luxury sedan with leather seats, ambient lighting, and advanced safety features.",
                "image": url + "executive_sedan.png",
                "image_description": "Luxury executive sedan in front of a hotel",
                "distance": "750 km",
                "passengers": "4",
                "trunk": "450 l",
                "pricePerDay": "ab 200 €",
                "pricePerWeek": "ab 1200 €",
                "features": "3.0L engine, adaptive suspension, massage seats"
            },
            {
                "id": "10",
                "title": "Luxury SUV",
                "description": "A premium SUV with spacious interior, panoramic roof, and high-end entertainment system.",
                "image": url + "luxury_suv.png",
                "image_description": "Luxury SUV parked near a scenic overlook",
                "distance": "700 km",
                "passengers": "5",
                "trunk": "650 l",
                "pricePerDay": "ab 220 €",
                "pricePerWeek": "ab 1320 €",
                "features": "3.5L engine, surround sound, heated rear seats"
            }
            ]
        
        return responses