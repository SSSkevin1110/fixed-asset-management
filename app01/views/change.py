import datetime
import threading
import time
import pytz
from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class AssetChangeInfo(BootStrapModelForm):
    class Meta:
        model = models.AssetChangeInfo
        fields = "__all__"
        exclude = ['now_type', 'confirmed']  # 确保 'confirmed' 不被前端修改

    def __init__(self, *args, **kwargs):
        super(AssetChangeInfo, self).__init__(*args, **kwargs)
        self.fields['OriginalUnit'].queryset = models.Department.objects.all()


def asset_change_list(request):
    """显示转让信息"""
    form = AssetChangeInfo()
    queryset = models.AssetChangeInfo.objects.select_related('OriginalUnit', 'NowUnit').all()
    page_object = Pagination(request, queryset, page_size=10)
    return render(request, 'asset_change_list.html',
                  {'form': form, 'queryset': page_object.page_queryset, "page_string": page_object.html()})


def asset_change_add(request):
    """登记转让信息"""
    if request.method == 'GET':
        form = AssetChangeInfo()
        if request.session['info']['type'] == 1:
            context = {
                'form': form,
            }
            return render(request, 'asset_change_add.html', context)
        else:
            return render(request, 'u_asset_change_add.html', {'form': form})
    form = AssetChangeInfo(data=request.POST)
    if form.is_valid():
        form.save()
        if request.session['info']['type'] == 1:
            return redirect('/asset/change')
        else:
            return redirect('/user/')
    return HttpResponse(''.join(form.errors))


def asset_change_del(request, nid):
    """删除"""
    models.AssetChangeInfo.objects.filter(id=nid).delete()
    return redirect('/asset/change/')


@csrf_exempt
def info_verify(request, Reg_number):
    """确认"""
    if request.session.get('info', {}).get('type') == 1:
        asset = models.AssetChangeInfo.objects.filter(Reg_number=Reg_number).first()
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
            ti = now - datetime.timedelta(minutes=15)
            # 每1分钟执行一次
            # 获取未确认的数据
            li = models.AssetChangeInfo.objects.filter(now_type=0)
            for i in li:
                # 如果创建时间小于 ti 删除
                if i.create_time < timezone.make_aware(ti, pytz.UTC):
                    i.delete()
            time.sleep(60)
        except Exception as e:
            time.sleep(1)


threading.Thread(target=check_model).start()
