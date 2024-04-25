from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5
from django.utils import timezone
import random
import datetime
from datetime import datetime
from app01.utils.pagination import Pagination


def user_asset(request):
    """资产信息展示(用户)"""
    search_field = request.GET.get('search_field', 'name')
    search_data = request.GET.get('q', "")
    data_dict = {}

    # 根据下拉框选择的字段来设置查询参数
    if search_data:
        if search_field == 'name':
            data_dict["Name__icontains"] = search_data
        elif search_field == 'model':
            data_dict["Model__icontains"] = search_data
        elif search_field == 'reg_num':
            data_dict["Registration_number__icontains"] = search_data

    queryset = models.AssetsInfo.objects.filter(**data_dict)
    # print(queryset)
    page_object = Pagination(request, queryset)
    content = {
        "search_data": search_data,
        "data_list": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, "u_asset_list.html", content)


# class AssetInfoForm(BootStrapModelForm):
#     class Meta:
#         model = models.AssetsInfo
#         fields = "__all__"
#         exclude = ['now_type']


# def generate_unique_registration_number():
#     a = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
#     return a
#     # return uuid.uuid4()
# def asset_add(request):
#     if request.method == 'GET':
#         # 生成唯一的登记编号
#         registration_number = generate_unique_registration_number()
#         # 将登记编号传递给表单初始化时的初始数据
#         form = AssetInfoForm(initial={'Registration_number': registration_number})
#
#         if request.session['info']['type'] == 1:
#             return render(request, 'asset_add.html', {'form': form})
#         else:
#             return render(request, 'u_asset_add.html', {'form': form})
#
#     form = AssetInfoForm(data=request.POST)
#     if form.is_valid():
#         form.instance.Registration_number = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
#         form.instance.admin_id = request.session["info"]["id"]
#         form.save()
#     else:
#         return HttpResponse("数据不合法")
#     if request.session['info']['type'] == 1:
#         return redirect('/asset/')
#     else:
#         return redirect('/user/')
#     return JsonResponse(data)