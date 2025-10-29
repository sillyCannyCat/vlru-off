from ninja import Router
from api.schemas.complaints import ComplaintSummaryOut, ComplaintGraphOut, ComplaintGraphItem
from api.schemas.errors import ErrorSchema
from api.services.complaints import get_complaints
from django.utils import timezone
from datetime import timedelta
router = Router(tags=['complaints'])
@router.get('/', response={200: ComplaintSummaryOut, 500: ErrorSchema})
async def complaints_summary(request):
    _type_vals = {
        'HT': 'Heat',
        'HW': 'Hot water',
        'CW': 'Cold water',
        'EL': 'Electricity'
    }
    complaints_data = get_complaints(request)
    count = 0
    _types = list()
    for item in complaints_data:
        _types.append(_type_vals[item[0]])
        count += item[-1]
    return {
        'report_date' : timezone.now().date,
        'summary':_types,
        'complaint_count':count,
        'created_at':timezone.now()
    }