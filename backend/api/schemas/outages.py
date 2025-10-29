from ninja import Schema
from typing import List, Dict

class OutageTypeStat(Schema):
    value: int

class OrganizationStat(Schema):
    id: int
    name: str
    value: int

class OutagesStatsOut(Schema):
    types: Dict[str, OutageTypeStat]
    organizations: List[OrganizationStat]

class TodayStatsOut(Schema):
    date: str
    today_count: int
    yesterday_count: int
    planned_count: int
    difference: int
    difference_percent: int
    trend: str
