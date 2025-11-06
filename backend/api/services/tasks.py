import api.models as models
import random
from datetime import timedelta
from django.utils import timezone
from background_task import background


@background(schedule=60*60*24)
def add_data_to_models():
    try:
        print("here 1")
        for black_type in ['HT', 'HW', 'CW', 'EL']:
            start_days = random.randrange(1, 365, 1)
            end_days = random.randrange(1, 365, 1)
            initiator_type = random.choice([0, 1])
            if initiator_type == 1:
                blackout = models.Blackout.objects.create(
                    start_date=timezone.now() + timedelta(hours=10) - timedelta(days=start_days),
                    end_date=timezone.now()+ timedelta(hours=10) + timedelta(days=end_days),
                    type=black_type,
                    initiator_id=None,
                    source_id=None,
                    description=None
                )
            else:
                blackout = models.Blackout.objects.create(
                    start_date=timezone.now() + timedelta(hours=10) - timedelta(days=start_days),
                    end_date=timezone.now() + timedelta(hours=10) + timedelta(days=end_days),
                    type=black_type,
                    initiator_id=models.Initiator.objects.all().order_by('?'),
                    source_id=models.Source.objects.all().order_by('?'),
                    description=None
                )
            print("here 2")
            count = random.choice(range(100, 1000, 1))
            for build in models.Building.objects.all().order_by('?')[:count]:
                models.BlackoutBuilding.objects.create(
                    blackout_id = blackout,
                    building_id = build
                )
        print('Good')
    except Exception:
        raise(Exception)