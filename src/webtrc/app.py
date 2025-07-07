import os
import logging
from aiohttp import web
import aiohttp
import asyncio

from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv 
from config import CONFIG
from rentaldb import RentalDBStore

load_dotenv(override=True) # take environment variables from .env.

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_ROOT, 'Static')

# Load open ai environment variables
WEBRTC_URL = os.environ.get("AZURE_OPENAI_WEBRTC_URL")
SESSIONS_URL = os.environ.get("AZURE_OPENAI_WEBRTC_SESSIONS_URL")
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
#get voice from CONFIG
VOICE = CONFIG.get("VOICE")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

rental_db = RentalDBStore()

@routes.get('/')
async def index(request):
    return web.FileResponse(os.path.join(STATIC_DIR, 'index.html'))

@routes.get('/{filename:.+\\.js}')
async def serve_js(request):
    filename = request.match_info['filename']
    file_path = os.path.normpath(os.path.join(STATIC_DIR, filename))

    # Security check to prevent directory traversal
    if not file_path.startswith(STATIC_DIR):
        logger.warning(f"Directory traversal attempt for JS file: {filename}")
        return web.Response(status=403, text="Forbidden")

    if os.path.isfile(file_path):
        return web.FileResponse(file_path)
    else:
        logger.warning(f"JS file not found at path: {file_path}. Requested filename: {filename}. CWD: {os.getcwd()}")
        return web.Response(status=404, text="Not Found")

@routes.get('/{filename:.+\\.css}')
async def serve_css(request):
    filename = request.match_info['filename']
    file_path = os.path.normpath(os.path.join(STATIC_DIR, filename))

    # Security check to prevent directory traversal
    if not file_path.startswith(STATIC_DIR):
        logger.warning(f"Directory traversal attempt for CSS file: {filename}")
        return web.Response(status=403, text="Forbidden")

    if os.path.isfile(file_path):
        return web.FileResponse(file_path)
    else:
        logger.warning(f"CSS file not found at path: {file_path}. Requested filename: {filename}. CWD: {os.getcwd()}")
        return web.Response(status=404, text="Not Found")

@routes.post('/api/search/locations')
async def search_locations(request):
    input = await request.json()
    locations = await rental_db.get_available_locations(input)
    return web.Response(text=locations)

@routes.post('/api/search/cars')
async def search_cars(request):
    input = await request.json()
    cars = await rental_db.get_available_cars(input)
    return web.Response(text=cars)

@routes.post('/start-session')
async def start_session(request):
    payload = {
        "model": DEPLOYMENT,
        "voice": VOICE
    }

    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(SESSIONS_URL, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    logger.error(f"Session API error: {error_text}")
                    return web.json_response({"error": "API request failed", "details": error_text}, status=500)
                data = await resp.json()
                session_id = data.get("id")
                ephemeral_key = data.get("client_secret", {}).get("value")
                logger.info(f"Ephemeral key: {ephemeral_key}")
                return web.json_response({"session_id": session_id, "ephemeral_key": ephemeral_key})
    except Exception as e:
        logger.exception("Error fetching ephemeral key:")
        return web.json_response({"error": str(e)}, status=500)

@routes.post('/webrtc-sdp')
async def webrtc_sdp(request):
    data = await request.json()
    ephemeral_key = data['ephemeral_key']
    offer_sdp = data['offer_sdp']
    headers = {
        "Authorization": f"Bearer {ephemeral_key}",
        "Content-Type": "application/sdp"
    }
    url = f"{WEBRTC_URL}?model={DEPLOYMENT}"


    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=offer_sdp, headers=headers) as resp:
                #check if the response is anything other than 200s
                if resp.status < 200 or resp.status >= 300:
                    error_text = await resp.text()
                    logger.error(f"WebRTC SDP exchange failed: {error_text}")
                    return web.json_response({"error": "WebRTC SDP exchange failed", "details": error_text}, status=500)
                answer_sdp = await resp.text()
                return web.json_response({'answer_sdp': answer_sdp})
    except Exception as e:
        logger.exception("Error in WebRTC SDP exchange:")
        return web.json_response({"error": str(e)}, status=500)

@routes.get('/config')
async def get_config(request):
    """Serve the CONFIG constants as JSON to the frontend."""
    return web.json_response(CONFIG)

async def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(create_app(), port=8080, host='127.0.0.1')
