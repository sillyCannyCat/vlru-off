from ninja import NinjaAPI
from api.routers.maps import router as maps_router
from api.routers.outages import router as outages_router
from api.routers.complaints import router as complaints_router

api = NinjaAPI(title='Blackout API', version='1.0.0')

api.add_router('/maps/', maps_router)
api.add_router('/outages/', outages_router)
api.add_router('/complaints/', complaints_router)
