from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from utils.custome_response import CustomeResponse


def exception_handler(exc,context):
    """
    自定义异常处理
    :param exc: 别的地方抛的异常就会传给exc
    :param context: 字典形式。抛出异常的上下文(即抛出异常的出处;即抛出异常的视图)
    :return: Response响应对象
    """
    response = drf_exception_handler(exc,context)
    if response is None:
        # drf 处理不了的异常
        print('%s - %s - %s' % (context['view'], context['request'].method, exc))
        return CustomeResponse({'detail': '服务器错误'}, code=500,msg="服务器内部错误",status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    if isinstance(exc,ValidationError):
        message = ""
        data = response.data
        for key in data:
            message += ";".join(data[key])
        return CustomeResponse(None,code="9999",msg=message)
    return response