import django_filters
from rest_framework import generics
from rest_framework.response import Response

from guoya_api.common.automation_case import run_api
from . import serializers
from . import models
from .filters import ProjectFilter
from rest_framework import filters
from . import pagination
from rest_framework import mixins
from rest_framework import views


class Projects(generics.GenericAPIView):
    queryset = models.Project.objects.all()  # 获取列表视图的查询集
    serializer_class = serializers.ProjectSerializer  # 视图使用的序列化器
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # 针对某个GenericAPIView视图添加过滤

    def get(self, request, *args, **kwargs):
        """
        获取项目列表所有的数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 返回视图使用的查询集，是列表视图与详情视图获取数据的基础，默认返回 queryset属性，可以重写
        courses = self.get_queryset()
        # 返回序列化器对象，被其他视图或扩展类使用，如果我们在视图中想要获取序列化器对象，可以直接调用此方法。
        serializer = self.get_serializer(instance=courses, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        新增项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data  # 校验请求数据
        serializer = serializers.ProjectSerializer(data=data)  # 执行反序列化过程
        # 调用is_valid()方法进行验证，验证成功返回True，否则返回False。
        # 验证数据是否符合要求，raise_exception=True指定不符合条件时自动抛出异常
        serializer.is_valid(raise_exception=True)
        serializer.save()  # 提交到数据库中
        return Response(serializer.validated_data)


# DestroyModelMixin 删除单个视图 删除一个存在的数据对象
# UpdateModelMixin 更新视图 更新一个存在的数据对象
# GenericAPIView 查询单个或者查询全部的数据对象 新增数据对象
# UpdateModelMixin 更新单个项目
# DestroyModelMixin 删除单个项目

class Project(generics.GenericAPIView):
    queryset = models.Project.objects.all()  # 获取列表视图的查询集
    serializer_class = serializers.ProjectSerializer  # 视图使用的序列化器
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter]  # 针对某个GenericAPIView视图添加过滤
    filterset_class = ProjectFilter  # 指定查询类,设置查询关键字name 支持模糊查询
    # ordering_fields = ['id']  # 不指定则默认序列化器上的任何可读字段都可用来排序
    ordering = ['-id']  # 使用ordering属性指定默认排序字段
    pagination_class = pagination.PageNumberPagination  # 1. 指定分页器对象

    def get(self, request, *args, **kwargs):
        '''
        模糊查询单个项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        # 1.使用filter_queryset方法对查询集进行过滤
        project = self.filter_queryset(self.get_queryset())
        # 2. 使用自己配置的分页器调用分页方法进行分页
        project_data = self.paginate_queryset(project)
        # 3.序列化我们分页好的数据
        serializer = self.get_serializer(instance=project_data, many=True)
        return Response(serializer.data)


class Project1(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectDeserializer

    def get(self, request, *args, **kwargs):
        '''
        查询单个项目的详细信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        project = self.get_object()
        return Response(serializers.ProjectSerializer(instance=project).data)

    def put(self, request, *args, **kwargs):
        '''
        修改单个项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        '''
        # 删除单个项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.destroy(request, *args, **kwargs)


class TestCases(views.APIView):
    def post(self, request):
        data = request.data  # APIView中对httprequest进行二次封装，提供了request.data和request.query_params常用属性
        headers = data.pop('headDict')  # 取出并删除data中headDict字段的数据
        raw_data = data.pop("requestList")  # 因为requestList不存进数据库表中,所以满足条件就去除requestList的值
        project_id = data.pop("project_id")
        regularParam = data.pop("RegularParam")
        '''
        1.外键关联序列化的时候需要先获取外键对象
        2.调用save方法的时候把对象传过去
        '''
        # 获取外键对象
        obj = models.AutomationTestCase.objects.get(id=data.pop("automationTestCase_id"))
        # 把接口详细信息存入automationcaseapi表中
        serializer = serializers.AutomationCaseApiDeserializer(data=data)  # 构建序列化对象 实例用instance 非实例用data
        serializer.is_valid(raise_exception=True)  # 验证数据是否有效
        test_case = serializer.save(automationTestCase=obj)  # 写入更新至数据库表中
        for i in headers:
            if i["name"] == "":
                continue
            serializer = serializers.AutomationHeadDeserializer(data=i)
            serializer.is_valid(raise_exception=True)  # 验证数据是否有效
            serializer.save(automationCaseApi=test_case)  # 写入更新至数据库表中
        if data["requestParameterType"] == "raw":  # 判断requestParameterType的值是否为"raw"
            # 将requestList字段的字符串数据转换成字典数据,并把生成的case_api_id跟guoya_api_automationparameterraw的id做关联
            raw = {"data":raw_data}
            # 反序列化操作提交到api_test_automationparameterraw这张表中
            serializer = serializers.AutomationParameterRawDeserializer(data=raw)
            serializer.is_valid(raise_exception=True)  # 验证数据是否有效
            serializer.save(automationCaseApi=test_case)  # 写入更新至数据库表中
        elif(data["requestParameterType"] == "form-data"):
            for i in raw_data:
                serializer = serializers.AutomationParameterDeserializer(data=i)
                serializer.is_valid(raise_exception=True)
                serializer.save(automationCaseApi=test_case)
        return Response("ok")


class ExcuteCase(views.APIView):
    def post(self,request):
        # 获取请求数据
        data = request.data
        # 获取执行的接口id
        api_id = data["api_id"]
        # 获取使用主机id
        host_id = data["host_id"]
        # 校验接口数据是否存在,是否有缺失
        # 获取接口请求之后的响应数据
        run_api(api_id=api_id,host_id=host_id)
        # 根据id获取指定的查询集
        case_api = models.AutomationCaseApi.objects.filter(id=api_id).first()
        # 根据查询集的关联名字获取关联表指定的数据,取最后一条数据
        res = case_api.test_result.all().last()
        # 将获取的数据序列化
        serializer = serializers.AutomationTestResultSerializer(instance=res)
        return Response(serializer.data)
