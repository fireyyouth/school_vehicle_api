from .models import BulletinBoard
from rest_framework import serializers


class BulletinBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletinBoard
        fields = ['id', 'content', 'update_time']