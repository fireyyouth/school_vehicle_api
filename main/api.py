from ninja import Router, Schema
from ninja.schema import Schema
from django.contrib import auth
from ninja.errors import HttpError
from django.contrib.auth.decorators import permission_required
from .models import *
from django.db.utils import IntegrityError
from collections import defaultdict
from faker import Faker
router = Router()

class LoginSchema(Schema):
    identifier: str
    password: str

@router.post('/login')
def login(request, login_info: LoginSchema, role: str):
    if role == 'teacher':
        user = auth.authenticate(identifier=login_info.identifier, password=login_info.password)
        if user is None:
            raise HttpError(401, '用户名或密码错误')
    elif role == 'visitor':
        user, created = User.objects.get_or_create(identifier=login_info.identifier, password='', role='visitor')
        if created:
            user.username = Faker(locale='zh_CN').name()
            user.save()
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


from ninja.security import django_auth

@router.get('/parking_spot', auth=django_auth)
def get_parking_spot(request, start_time: datetime, end_time: datetime):
    print('get_parking_spot', start_time, end_time)
# @permission_required(['main.view_parking_spot', 'main.view_parkingspotreservation'], raise_exception=True)
    # [amin, amax] and [bmin, bmax] overlap iff (amin < bmax AND bmin < amax)
    reserved_spots = ParkingSpotReservation.objects.filter(status='active', start_time__lt=end_time, end_time__gt=start_time) \
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

@router.post('/parking_spot/reservation', auth=django_auth)
def reserve_parking_spot(request, spot_number: int, start_time: datetime, end_time: datetime, vehicle_id: int):
    print('reserve_parking_spot', spot_number, start_time, end_time, vehicle_id)
    vehicle = Vehicle.objects.get(id=vehicle_id)
    if vehicle.owner != request.user:
        raise HttpError(403, '无权限')
    ParkingSpotReservation.objects.create(
        vehicle=vehicle,
        parking_spot=ParkingSpot.objects.get(spot_number=spot_number),
        start_time=start_time,
        end_time=end_time,
        status='active'
    )
    return {
        'detail': '预约成功'
    }

@router.post('/parking_spot/reservation/{reservation_id}', auth=django_auth)
def update_parking_reservation(request, reservation_id: int, status: str):
    print('update_parking_reservation_status', reservation_id, status)
    reservation = ParkingSpotReservation.objects.get(id=reservation_id)
    if reservation.vehicle.owner != request.user:
        raise HttpError(403, '无权限')
    reservation.status = status
    reservation.save()
    return {
        'detail': '预约状态更新成功'
    }

@router.get('/parking_spot/reservation', auth=django_auth)
def get_parking_reservation(request):
    if request.user.role == 'admin':
        reservations = ParkingSpotReservation.objects.all()
    else:
        reservations = ParkingSpotReservation.objects.filter(vehicle__owner=request.user)
    return {
        'data': [
            {
                'id': reservation.id,
                'parking_spot': reservation.parking_spot.spot_number,
                'vehicle': reservation.vehicle.number,
                'owner': reservation.vehicle.owner.username,
                'start_time': reservation.start_time,
                'end_time': reservation.end_time,
                'status': reservation.status
            } for reservation in reservations
        ]
    }

@router.post('/vehicle', auth=django_auth)
def register_vehicle(request, number: str, vehicle_type: str, brand: str):
    try:
        Vehicle.objects.create(
            number=number,
            vehicle_type=vehicle_type,
            brand=brand,
            owner=request.user
        )
        return {
            'detail': '车辆注册成功'
        }
    except IntegrityError:
        raise HttpError(400, '车辆已存在')

@router.get('/vehicle', auth=django_auth)
def get_vehicle(request):
    if request.user.role == 'admin':
        vehicles = Vehicle.objects.all()
    else:
        vehicles = Vehicle.objects.filter(owner=request.user)
    return {
        'data': [
            {
                'id': vehicle.id,
                'number': vehicle.number,
                'vehicle_type': vehicle.vehicle_type,
                'brand': vehicle.brand,
                'owner': vehicle.owner.username,
                'register_time': vehicle.register_time,
                'update_time': vehicle.update_time
            } for vehicle in vehicles
        ]
    }

@router.delete('/vehicle/{vehicle_id}', auth=django_auth)
def delete_vehicle(request, vehicle_id: int):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    return {
        'detail': '车辆删除成功'
    }

@router.get('/passage_log', auth=django_auth)
def get_passage_log(request):
    if request.user.role != 'admin':
        raise HttpError(403, '无权限')
    return {
        'data': [
            {
                'vehicle_number': log.vehicle_number,
                'vehicle_type': log.vehicle_type,
                'gate': log.gate,
                'direction': log.direction,
                'create_time': log.create_time
            } for log in PassageLog.objects.all()
        ]
    }

@router.get('/parking_log', auth=django_auth)
def get_parking_log(request):
    if request.user.role != 'admin':
        raise HttpError(403, '无权限')
    return {
        'data': [
            {
                'vehicle_number': log.vehicle_number,
                'vehicle_type': log.vehicle_type,
                'parking_spot': log.parking_spot.spot_number,
                'event': log.event,
                'create_time': log.create_time
            } for log in ParkingLog.objects.all()
        ]
    }

@router.post('/visit_reservation', auth=django_auth)
def create_visit_reservation(request, vehicle_number: str, date: datetime):
    if request.user.role != 'visitor':
        raise HttpError(403, '无权限')
    VisitReservation.objects.create(
        visitor=request.user,
        vehicle_number=vehicle_number,
        date=date,
        status='created'
    )
    return {
        'detail': '预约成功'
    }

@router.post('/visit_reservation/{reservation_id}', auth=django_auth)
def update_visit_reservation(request, reservation_id: int, status: str):
    if request.user.role not in ['visitor', 'admin']:
        raise HttpError(403, '无权限')
    reservation = VisitReservation.objects.get(id=reservation_id)
    reservation.status = status
    reservation.save()
    return {
        'detail': '状态更新成功'
    }

@router.get('/visit_reservation', auth=django_auth)
def get_visit_reservation(request):
    if request.user.role == 'admin':
        reservations = VisitReservation.objects.all()
    elif request.user.role == 'visitor':
        reservations = VisitReservation.objects.filter(visitor=request.user)
    else:
        raise HttpError(403, '无权限')
    return {
        'data': [
            {
                'id': reservation.id,
                'visitor': reservation.visitor.username,
                'vehicle_number': reservation.vehicle_number,
                'date': reservation.date,
                'status': reservation.status,
                'create_time': reservation.create_time,
                'update_time': reservation.update_time
            } for reservation in reservations
        ]
    }
