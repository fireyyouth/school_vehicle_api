from main.models import *
from bulletin.models import *
from django.utils import timezone
from django.contrib.auth.models import Group
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker(locale='zh_CN')

def init_group():
    Group.objects.create(name='teacher').save()


def init_user():
    User.objects.create_superuser(identifier='00000000', password='00000000', role='admin', username='管理员')
    User.objects.create_user(identifier='00000001', password='00000001', role='teacher', username='张老师', gender='男', email=fake.email(), phone=fake.phone_number())
    User.objects.create_user(identifier='00000002', password='00000002', role='teacher', username='李老师', gender='女', email=fake.email(), phone=fake.phone_number())

def init_vehicle():
    Vehicle.objects.create(number='京A00001', owner=User.objects.get(identifier='00000001'), vehicle_type='轿车', brand='宝马')
    Vehicle.objects.create(number='京A00002', owner=User.objects.get(identifier='00000002'), vehicle_type='轿车', brand='奔驰')

def init_parking_spot():
    for i in range(1, 21):
        ParkingSpot.objects.create(spot_number=i, district='东校区')
    for i in range(21, 41):
        ParkingSpot.objects.create(spot_number=i, district='西校区')

def init_bulletin_board():
    BulletinBoard.objects.create(content='本条公告内容为测试使用')

def generate_vehicle_number():
    return random.choice('京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁') + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + str(random.randint(10000, 99999))

def generate_time_points(base_date, count):
    # 每小时段及其出现权重（数值越大，生成的概率越高）
    hour_weights = {
        0: 1, 1: 0.5, 2: 0.3, 3: 0.2, 4: 0.3, 5: 1,
        6: 3, 7: 6, 8: 10, 9: 6, 10: 4, 11: 3,
        12: 3, 13: 4, 14: 5, 15: 5,
        16: 6, 17: 9, 18: 10, 19: 6,
        20: 3, 21: 2, 22: 1, 23: 0.5
    }

    # 把小时和权重变成两个列表
    hours, weights = zip(*hour_weights.items())

    time_points = []
    for _ in range(count):
        hour = random.choices(hours, weights=weights)[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        time_points.append(base_date + timedelta(hours=hour, minutes=minute, seconds=second))
    return time_points


def init_passage_log():
    vehicle_type_weights = {
        '自行车': 5,
        '汽车': 3,
        '校车': 1
    }
    vehicle_types, weights = zip(*vehicle_type_weights.items())

    today = datetime.now(tz=timezone.get_current_timezone()).replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range(7):
        print('create passage log for', today - timedelta(days=i))
        time_points = generate_time_points(today - timedelta(days=i), 100)
        for time_point in time_points:
            PassageLog.objects.create(
                vehicle_number=generate_vehicle_number(),
                vehicle_type=random.choices(vehicle_types, weights=weights)[0],
                gate=random.choice(['东门', '西门', '北门', '南门']),
                direction=random.choice(['进校', '出校']),
                create_time=time_point
            )

def main():
    init_group()
    init_user()
    init_vehicle()
    init_parking_spot()
    init_bulletin_board()
    init_passage_log()
    print('populate done')

main()
