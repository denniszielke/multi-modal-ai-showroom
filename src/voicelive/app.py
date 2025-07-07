import logging
import os
from pathlib import Path
from aiohttp import web
from azure.core.credentials import AzureKeyCredential
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from dotenv import load_dotenv

from rentaldb import RentalDBStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webrtc")

if not os.environ.get("RUNNING_IN_PRODUCTION"):
    logger.info("Running in development mode, loading from .env file")
    load_dotenv()
llm_endpoint = os.environ.get("SMALL_ENDPOINT")
llm_deployment = os.environ.get("SMALL_COMPLETION_MODEL")
llm_api_version = os.environ.get("SMALL_API_VERSION")

rental_db = RentalDBStore()

async def create_app():
    app = web.Application()

    # Serve static files and index.html
    current_directory = Path(__file__).parent  # Points to 'app' directory
    static_directory = current_directory / 'static'

    # Ensure static directory exists
    if not static_directory.exists():
        raise FileNotFoundError("Static directory not found at expected path: {}".format(static_directory))

    # Serve index.html at root
    async def index(request):
        return web.FileResponse(static_directory / 'index.html')

    app.router.add_get('/', index)
    app.router.add_static('/static/', path=str(static_directory), name='static')
    app.router.add_post("/api/search/locations", search_locations)
    app.router.add_post("/api/search/cars", search_cars)

    return app

async def search_locations(request):
    input = await request.json()
    locations = await rental_db.get_available_locations(input)
    return web.json_response(locations)

async def search_cars(request):
    input = await request.json()
    cars = await rental_db.get_available_cars(input)
    return web.json_response(cars)

if __name__ == "__main__":
    host = os.environ.get("HOST", "localhost")
    port = int(os.environ.get("PORT", 8765))
    web.run_app(create_app(), host=host, port=port)
