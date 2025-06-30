import logging
import os
from pathlib import Path
from aiohttp import web
from azure.core.credentials import AzureKeyCredential
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from dotenv import load_dotenv

from backend.tools import _show_final_details_tool_schema, _show_product_information_tool_schema,_get_available_locations_tool_schema, _get_available_models_tool_schema, Tool
from backend.rtmt import RTMiddleTier

from reportstore.rentaldb import RentalDBStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voicerag")

async def create_app():
    if not os.environ.get("RUNNING_IN_PRODUCTION"):
        logger.info("Running in development mode, loading from .env file")
        load_dotenv()
    llm_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    llm_deployment = os.environ.get("AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME")
    llm_key = os.environ.get("AZURE_OPENAI_API_KEY")

    credential = None
   
    if not llm_key:
        if tenant_id := os.environ.get("AZURE_TENANT_ID"):
            logger.info(
                "Using AzureDeveloperCliCredential with tenant_id %s", tenant_id)
            credential = AzureDeveloperCliCredential(
                tenant_id=tenant_id, process_timeout=60)
        else:
            logger.info("Using DefaultAzureCredential")
            credential = DefaultAzureCredential()
    llm_credential = AzureKeyCredential(llm_key) if llm_key else credential

    store = RentalDBStore()  
    
    app = web.Application()

    rtmt = RTMiddleTier(llm_endpoint, llm_deployment, llm_credential)

    rtmt.system_message = (
        "You are a helpful assistant working in a car rental company and are tasked to help the user make a rental car choice.\n"
        "The user is interesting in renting a car and needs to decide the pickup location, prefered car type, pick up and return date.\n"
        "You MUST start the converstation by introducing your self and explain the user that you will be asking questions to help him narrow down their choices.\n"
        "You should ask the user for the prefered pickup location and use the get_available_locations tool to propose the two closest locations.\n"
        "After the user has selected his prefered pickup location you should ask the user for pickup and return date and then retrieve the available car with the get_available_cars tool.\n"
        "After the user has selected his prefered car you should ask the user for the car model and use the show_model_information tool to show the user the car information. Help the user make the right car choice by asking for the required number of seats and the transmission type they need.\n"
        "You must engage the user in a friendly conversation, follow his interest and guide the user along while making sure you use the show_model_information when the user changes his preference to a different car model. The user will provide the answers to the questions." \
        "Once the user has selected the car model you should use the show_final_details tool to show the user the final details of his rental.\n"
    )
    rtmt.tools["get_available_locations"] = Tool(
        schema=_get_available_locations_tool_schema,
        target=lambda args: store.get_available_locations(args),
    )
    rtmt.tools["get_available_cars"] = Tool(
        schema=_get_available_models_tool_schema,
        target=lambda args: store.get_available_cars(args),
    )
    rtmt.tools["show_model_information"] = Tool(
        schema=_show_product_information_tool_schema,
        target=lambda args: store.show_product_information(args),
    )
    rtmt.tools["show_final_details"] = Tool(
        schema=_show_final_details_tool_schema,
        target=lambda args: store.show_final_details(args),
    )  
        
    rtmt.attach_to_app(app, "/realtime")

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

    return app

if __name__ == "__main__":
    host = os.environ.get("HOST", "localhost")
    port = int(os.environ.get("PORT", 8765))
    web.run_app(create_app(), host=host, port=port)
