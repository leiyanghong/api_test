import json

import requests

from .. import serializers
from .. import models


def run_api(api_id, host_id, ):
    # 从数据库获取ip和端口
    host = models.GlobalHost.objects.filter(id=host_id).first().host
    # 根据api_id获取指定的数据集
    case_api = models.AutomationCaseApi.objects.filter(id=api_id).first()
    '''
    获取请求方法
    '''
    # 将获取的查询集数据转换成字典数据
    data = serializers.AutomationCaseApiSerializer(instance=case_api).data
    request_method = data["requestType"].upper()
    # 也可以直接取值 upper()小写转换成大写字母
    # request_method = case_api.requestType.upper()
    url = data["httpType"].lower() + "://" + host + data["apiAddress"]
    response = None
    param = None
    json_data = None
    '''
    获取请求头数据
    '''
    # 多表关联根据关联名字header查询出所有的数据集
    header_objs = case_api.header.all()
    # 字典推导式获取name和value存进字典headers
    headers = {i.name: i.value for i in header_objs}
    '''
    获取请求数据
    '''
    if data["requestParameterType"] == "form-data":
        # 根据relate_name=parameterList获取所有的键值对参数
        api_query_set = case_api.parameterList.all()
        param = {i.name: i.value for i in api_query_set}
        response = send_request(method=request_method, url=url, params=param, headers=headers)
    elif (data["requestParameterType"] == "raw"):
        # 根据relate_name=parameterRaw获取所有的键值对参数
        api_body = case_api.parameterRaw
        # 将获取的字符串数据转换成字典格式的数据
        json_data = json.loads(api_body.data)
        # 发送请求
        response = send_request(method=request_method, url=url, data=json_data, headers=headers)
    # 获取接口响应数据
    response_headers= response.headers
    response_data = response.json()
    response_status_code = response.status_code
    models.AutomationTestResult(automationCaseApi=case_api,url=url,requestType=request_method,host=host,header=json.dumps(headers),
                                # 利用三目表达式,判断存储不同类型的数据格式,如果是params数据,将params的数据处理成键值对格式的字符串数据,以"&"隔开,反之取json_data的字符串数据
                                parameter="&".join(["{}={}".format(i,param[i]) for i in param])  if param is not None else json.dumps(json_data),
                                httpStatus=response_status_code,examineType=case_api.examineType,data=None,result="PASS",responseData=json.dumps(response_data)).save()

    return response_headers,response_data,response_status_code


# 发送请求
def send_request(method=None, url=None, params=None, data=None, headers=None):
    res = None
    if method == "POST":
        res = requests.request(method=method, url=url, data=data, json=data, headers=headers)
    elif (method == "GET"):
        res = requests.request(method=method, url=url, params=params, headers=headers)
    elif (method == "PUT"):
        pass
    elif (method == "DELETE"):
        pass
    return res
