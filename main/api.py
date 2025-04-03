from ninja import Router, Schema
from ninja.schema import Schema
from django.contrib import auth
from ninja.errors import HttpError
from django.contrib.auth.decorators import permission_required
from .models import ParkingSpotReservation, ParkingSpot
from collections import defaultdict
router = Router()

class LoginSchema(Schema):
    identifier: str
    password: str
    role: str

@router.post('/login')
def login(request, login_info: LoginSchema):
    user = auth.authenticate(identifier=login_info.identifier, password=login_info.password)
    if user is None:
        raise HttpError(401, '用户名或密码错误')
    auth.login(request, user)
    return {
        'detail': '登录成功',
        'profile': {
            'username': user.username,
            'role': user.role,
            'identifier': user.identifier
        }
    }

@router.post('/logout')
def logout(request):
    auth.logout(request)
    return {
        'detail': '退出成功',
    }


import random
from datetime import datetime, timedelta

def generate_data():
    labels = []
    data = []
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    for i in range(24 * 30):  # Generate data for a month
        time = now - timedelta(hours=(24 * 30 - 1 - i))
        formatted_time = time.strftime('%m-%d %H:00')
        labels.append(formatted_time)
        data.append(random.randint(0, 99))

    chart_data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Count",
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 2,
                "hoverBackgroundColor": "rgba(75, 192, 192, 0.8)",
                "hoverBorderColor": "rgba(75, 192, 192, 1)",
                "data": data
            }
        ]
    }

    return chart_data

from ninja.security import django_auth

@router.get('/passagelog', auth=django_auth)
@permission_required('main.view_passagelog', raise_exception=True)
def get_passage_log(request):
    return {
        'data': generate_data()
    }

@router.get('/parking_spot', auth=django_auth)
def get_parking_spot(request, start_time: datetime, end_time: datetime):
    print('get_parking_spot', start_time, end_time)
# @permission_required(['main.view_parking_spot', 'main.view_parkingspotreservation'], raise_exception=True)
    # [amin, amax] and [bmin, bmax] overlap iff (amin <= bmax AND bmin <= amax)
    reserved_spots = ParkingSpotReservation.objects.filter(start_time__lte=end_time, end_time__gte=start_time) \
        .values('parking_spot') \
        .distinct() \
        .all()
    reserved_spots = set(stop['parking_spot'] for stop in reserved_spots)
    print('reserved_spots', reserved_spots)
    data = defaultdict(list)
    for spot in ParkingSpot.objects.all():
        data[spot.district].append({
            'id': spot.spot_number,
            'reserved': spot.id in reserved_spots
        })
    return {
        'data': data
    }

@router.post('/parking_spot/reserve', auth=django_auth)
def reserve_parking_spot(request, spot_number: int, start_time: datetime, end_time: datetime):
    print('reserve_parking_spot', spot_number, start_time, end_time)
    ParkingSpotReservation.objects.create(
        reserved_by=request.user,
        parking_spot=ParkingSpot.objects.get(spot_number=spot_number),
        start_time=start_time,
        end_time=end_time
    )
    return {
        'detail': '预约成功'
    }