from ninja import Router
from ..schemas.maps import MapResponse, MapPoint

router = Router()

@router.get("/", response=MapResponse)
def get_map_data(request):
    # запрос к БД, обработка и т.д.
    return {
        "points": [
            {"id": 1, "name": "Точка 1", "lat": 59.8944, "lon": 30.2642},
        ]
    }