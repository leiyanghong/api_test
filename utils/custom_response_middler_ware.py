class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
         # 配置和初始化

    def __call__(self, request):

        # 在这里编写视图和后面的中间件被调用之前需要执行的代码
        # 这里其实就是旧的process_request()方法的代码
        response = self.get_response(request)
        # if "code" not in response.data:
        #
        #     data = response.data
        #     response.data={
        #         "code":"0000",
        #         "message":"查询成功",
        #         "data":response.data
        #     }
        #     # 因返回时已经render过response，要想让这里的修改有效，需要手动在render一次
        # response._is_rendered = False
        # response.render()
        # response["content-length"]=len(response.content)
        # 在这里编写视图调用后需要执行的代码
        # 这里其实就是旧的 process_response()方法的代码
        return response

    def process_template_response(self, request, response):# 推荐
        if request.method=="DELETE" and response.data is None:
            response.data = {
                "code": "0000",
                "message": "删除成功",
                "data": response.data
            }

        if "code" not in response.data:
            # data = response.data
            response.data={
                "code":"0000",
                "message":"操作成功",
                "data":response.data
            }
        # 在这里编写视图调用后需要执行的代码
        # 这里其实就是旧的 process_response()方法的代码
        
        return response
