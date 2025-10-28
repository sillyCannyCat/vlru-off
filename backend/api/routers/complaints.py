from ninja import Router
from typing import List
from api.models import Complaint
from api.schemas.complaints import ComplaintSummaryOut, ComplaintGraphOut, ComplaintGraphItem
from api.schemas.errors import ErrorSchema
from django.utils import timezone
from datetime import timedelta
import pytz

router = Router(tags=['complaints'])

@router.get('/', response={200: ComplaintSummaryOut, 500: ErrorSchema})
async def complaints_summary(request):
    try:
        now = timezone.now()
        start = now - timedelta(hours=24)
        local_tz = pytz.timezone('Asia/Vladivostok')
        now_local = now.astimezone(local_tz)

        count = await Complaint.objects.filter(created_at__gte=start).acount()
        complaints = await Complaint.objects.filter(created_at__gte=start).all()

        type_counts = {"HW": 0, "CW": 0, "EL": 0}
        async for c in complaints:
            type_counts[c.type] += 1

        parts = []
        if type_counts["HW"] > 5: parts.append("горячей воды")
        if type_counts["CW"] > 5: parts.append("холодной воды")
        if type_counts["EL"] > 5: parts.append("света")

        if parts:
            if len(parts) > 1:
                summary = f"Жители сообщают о множественных отключениях {', '.join(parts[:-1])} и {parts[-1]}"
            else:
                summary = f"Жители сообщают о множественных отключениях {parts[0]}"
        else:
            summary = "Жалоб за последние 24 часа не поступало"

        return {
            "report_date": now.strftime("%Y-%m-%d"),
            "summary": summary,
            "complaint_count": count,
            "created_at": now_local.isoformat()
        }

    except Exception as e:
        return 500, {"message": "Ошибка сервера при обработке жалоб"}

@router.get('/graph/', response={200: ComplaintGraphOut, 400: ErrorSchema, 500: ErrorSchema})
async def complaints_graph(request, type: str = "24h"):
    if type not in ["24h", "60m"]:
        return 400, {"message": "Параметр 'type' должен быть '24h' или '60m'"}

    try:
        now = timezone.now()
        local_tz = pytz.timezone('Asia/Vladivostok')
        now_local = now.astimezone(local_tz)

        if type == "60m":
            total_minutes = 60
            interval_minutes = 5
            format_str = "%H:%M"
        else:
            total_minutes = 24 * 60
            interval_minutes = 60
            format_str = "%H:00"

        num_intervals = total_minutes // interval_minutes
        intervals = [
            now - timedelta(minutes=(total_minutes - i * interval_minutes))
            for i in range(num_intervals + 1)
        ]

        data = [
            {
                "time": point.astimezone(local_tz).strftime(format_str),
                "cold_water": 0,
                "hot_water": 0,
                "electricity": 0
            }
            for point in intervals
        ]

        start = now - timedelta(minutes=total_minutes)
        complaints = await Complaint.objects.filter(created_at__gte=start).all()
        type_map = {"CW": "cold_water", "HW": "hot_water", "EL": "electricity"}

        async for c in complaints:
            c_local = c.created_at.astimezone(local_tz)
            for i in range(len(intervals) - 1):
                if intervals[i] <= c_local < intervals[i + 1]:
                    key = type_map.get(c.type)
                    if key:
                        data[i][key] += 1
                    break
            else:
                key = type_map.get(c.type)
                if key:
                    data[-1][key] += 1

        return {"data": data}

    except Exception as e:
        return 500, {"message": "Ошибка при построении графика жалоб"}