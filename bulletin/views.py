from django.shortcuts import render
from rest_framework import generics
from .serializers import BulletinBoardSerializer
from .models import BulletinBoard
from rest_framework import mixins, viewsets

class BulletinBoardViewSet(
    mixins.ListModelMixin,       # GET /bulletin_board/ (list)
    mixins.UpdateModelMixin,     # PUT/PATCH /bulletin_board/<pk>/ (update)
    viewsets.GenericViewSet      # Base class (no default actions)
):
    queryset = BulletinBoard.objects.all()
    serializer_class = BulletinBoardSerializer