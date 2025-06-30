import logging
import os
from pathlib import Path
from aiohttp import web
from azure.core.credentials import AzureKeyCredential
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from dotenv import load_dotenv

from backend.tools import _get_available_categories_tool_schema, _get_product_variants_by_category_tool_schema, _get_product_models_by_variant_schema, _get_products_tool_schema, _show_product_categories_tool_schema, _show_product_information_tool_schema, _show_product_models_tool_schema, Tool
from backend.rtmt import RTMiddleTier

from reportstore.filedb import FileDBStore

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

    store: FileDBStore = None
    
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

    fileDB = FileDBStore()  
    
    app = web.Application()

    rtmt = RTMiddleTier(llm_endpoint, llm_deployment, llm_credential)

    rtmt.system_message = (
        "You are a helpful assistant that maintains a conversation with the user, while helping the user to make a choice for a car.\n"
        "The user is interesting in buying a car and needs to decide the engine category, the variations and the model.\n"
        "You MUST start the converstation by introducing your self and explain the user that you will be asking questions to help him narrow down their choices.\n"
        "Your first question should be to use the get_available_categories tool to find out possible product categories and related questions that you can use to help the user understand the difference between the cateogires.\n"
        "Make sure you use the show_product_categories tool to show the user the available categories and the options you have retrieved from the get_available_categories tool.\n"
        "If the users asks about product variations for find out about available options for a specific product for example different car types make sure you use the show_product_information tool to show the user the available variations and the options you have retrieved from the get_product_variants_by_category tool.\n"
        "Once the user is clear on the product variations you should help him to narrow the options for specific product model by retrieving available product models using the get_product_models_by_variant tool.\n"
        "You should use the get_products_by_category tool to retrieve possible vailable variations for the devices.\n"
        "You should should use the show_product_models and show_product_models tool to show the user the available product models.\n"
        "You must engage the user in a friendly conversation, follow his interest and guide the user along while making sure you use the show_product_information and show_product_models tool regularly when the user changes the conversation to a different product. The user will provide the answers to the questions."
    )
    rtmt.tools["get_available_categories"] = Tool(
        schema=_get_available_categories_tool_schema,
        target=lambda args: fileDB.get_available_categories(args),
    )
    rtmt.tools["get_product_variants_by_category"] = Tool(
        schema=_get_product_variants_by_category_tool_schema,
        target=lambda args: fileDB.get_product_variants_by_category(args),
    )
    rtmt.tools["get_product_models_by_variant"] = Tool(
        schema=_get_product_models_by_variant_schema,
        target=lambda args: fileDB.get_product_models_by_variant(args),
    )
    rtmt.tools["show_product_information"] = Tool(
        schema=_show_product_information_tool_schema,
        target=lambda args: fileDB.show_product_information(args),
    )
    rtmt.tools["show_product_categories"] = Tool(
        schema=_show_product_categories_tool_schema,
        target=lambda args: fileDB.show_product_categories(args),
    )
    rtmt.tools["show_product_models"] = Tool(
        schema=_show_product_models_tool_schema,
        target=lambda args: fileDB.show_product_models(args),
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
