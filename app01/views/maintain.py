import datetime
import threading
import time
import pytz
from django import forms
from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class AssetMaintainInfo(BootStrapModelForm):
    class Meta:
        model = models.AssetMaintainInfo
        fields = "__all__"
        exclude = ['now_type', 'confirmed']  # 确保 'confirmed' 不被前端修改


def asset_maintain_add(request):
    """登记维修信息"""
    if request.method == 'GET':
        form = AssetMaintainInfo()
        if request.session['info']['type'] == 1:
            context = {
                'form': form,
            }
            return render(request, 'asset_maintain_add.html', context)
        else:
            return render(request, 'u_asset_maintain_add.html', {'form': form})
    form = AssetMaintainInfo(data=request.POST)
    if form.is_valid():
        form.save()
        if request.session['info']['type'] == 1:
            return redirect('/asset/maintain')
        else:
            return redirect('/user/')
    return HttpResponse(''.join(form.errors))


def asset_maintain_list(request):
    """显示维修信息"""
    form = AssetMaintainInfo()
    queryset = models.AssetMaintainInfo.objects.all()
    page_object = Pagination(request, queryset, page_size=10)
    return render(request, 'asset_maintain_list.html',
                  {'form': form, 'queryset': page_object.page_queryset, "page_string": page_object.html()})


def asset_maintain_del(request, nid):
    """删除"""
    models.AssetMaintainInfo.objects.filter(id=nid).delete()
    return redirect('/asset/maintain/')


@csrf_exempt
def info_verify(request, Reg_number):
    """确认"""
    if request.session.get('info', {}).get('type') == 1:
        asset = models.AssetMaintainInfo.objects.filter(Reg_number=Reg_number).first()
        if asset:
            asset.now_type = 1
            asset.confirmed = True  # 修改确认状态
            asset.save()
            return HttpResponse('操作成功')
    return HttpResponse('没权限')

def check_model():
    while True:
        try:
            # 获取当前时间
            now = datetime.datetime.now()

            # 当前时间减去15分钟
            ti = now - datetime.timedelta(hours=24)
            # 每1分钟执行一次
            # 获取未确认的数据
            li = models.AssetMaintainInfo.objects.filter(now_type=0)
            for i in li:
                # 如果创建时间小于 ti 删除
                if i.create_time < timezone.make_aware(ti, pytz.UTC):
                    i.delete()
            time.sleep(60)
        except Exception as e:
            time.sleep(1)


# 启动线程执行上面的函数
threading.Thread(target=check_model).start()

