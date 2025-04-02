from ninja import NinjaAPI
from main.api import router as main_router

api = NinjaAPI()
api.add_router('/main', main_router)