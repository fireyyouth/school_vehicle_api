from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'bulletin_board', BulletinBoardViewSet)
