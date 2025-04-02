from ninja import NinjaAPI
from main.api import router as main_router
from django.core.exceptions import PermissionDenied

api = NinjaAPI()

@api.exception_handler(PermissionDenied)
def permission_denied_handler(request, exc):
    return api.create_response(request, {"detail": "权限不足"}, status=403)

api.add_router('/main', main_router)
