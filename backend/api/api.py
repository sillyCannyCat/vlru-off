from ninja import NinjaAPI
from api.routers.maps import router as maps_router
from api.routers.charts import router as charts_router
from api.routers.telegram import router as telegram_router

api = NinjaAPI(title='Blackout API', version='1.0.0')

api.add_router('/maps/', maps_router)
api.add_router('/charts/', charts_router)
api.add_router('/telegram/', telegram_router)