# 定义自己的查询类 实现模糊查询 精确查询
from django_filters import rest_framework as filters

from . import models


class ProjectFilter(filters.FilterSet):
    # field_name要过滤的字段 lookup_expr要过滤的规则
    name = filters.CharFilter(field_name="name", lookup_expr='contains')  # 对名字进行模糊查询
    type = filters.CharFilter(field_name="type")  # 对型号字段进行精确查询

    class Meta:
        model = models.Project
        fields = ['name', 'type']  # 指定查询参数
