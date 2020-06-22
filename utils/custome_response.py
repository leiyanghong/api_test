from rest_framework.response import Response


class CustomeResponse(Response):

    def __init__(self,*args,code='0000',msg="成功",**kwargs):
        # 格式化data
        data = {
            "code":code,
            "message":msg
        }
        if args is not None:
            data["data"]=args[0]
            kwargs["data"] = data
        elif "data" in kwargs:
            data["data"] = kwargs["data"]
            kwargs["data"]=data

        super().__init__(**kwargs)