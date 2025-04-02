from ninja import Router, Schema
from ninja.schema import Schema
from django.contrib import auth
from ninja.errors import HttpError

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
    }

@router.post('/logout')
def logout(request):
    auth.logout(request)
    return {
        'detail': '退出成功',
    }