import django_filters
from rest_framework import generics
from rest_framework.response import Response
from . import serializers
from . import models
from .filters import ProjectFilter
from rest_framework import filters
from . import pagination
from rest_framework import mixins


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

