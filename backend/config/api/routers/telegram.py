from ninja import Router
from ..schemas.telegram import TelegramLinkResponse

router = Router()

@router.get("/", response=TelegramLinkResponse)
def get_telegram_link(request):
    return {"url": "https://t.me/vlruoff_bot"}