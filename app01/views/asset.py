import datetime
from datetime import datetime
import threading
import time
import uuid
import pytz
from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import random
from decimal import Decimal
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination
from .maintain import AssetMaintainInfo
from .damage import AssetDamageInfo
from .change import AssetChangeInfo
from decimal import Decimal, ROUND_HALF_UP



class AssetInfoForm(BootStrapModelForm):
    class Meta:
        model = models.AssetsInfo
        fields = "__all__"
        exclude = ['now_type', 'confirmed']  # 确保 'confirmed' 不被前端修改


def asset(request):
    """资产数据显示"""
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
    page_object = Pagination(request, queryset)
    content = {
        "search_data": search_data,
        "data_list": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 页码
    }
    return render(request, "asset_list.html", content)


def generate_unique_registration_number():
    """生成唯一登记编号"""
    a = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
    return a
    # return uuid.uuid4()


def asset_add(request):
    """添加资产信息"""
    if request.method == 'GET':
        # 生成唯一的登记编号
        registration_number = generate_unique_registration_number()
        # 将登记编号传递给表单初始化时的初始数据
        form = AssetInfoForm(initial={'Registration_number': registration_number})

        if request.session['info']['type'] == 1:
            return render(request, 'asset_add.html', {'form': form})
        else:
            return render(request, 'u_asset_add.html', {'form': form})

    form = AssetInfoForm(data=request.POST)
    if form.is_valid():
        form.instance.Registration_number = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
    else:
        return HttpResponse("数据不合法")
    if request.session['info']['type'] == 1:
        return redirect('/asset/')
    else:
        return redirect('/user/')


class AssetEditInfoForm(BootStrapModelForm):
    Registration_number = forms.CharField(disabled=True, label='登记编号')

    class Meta:
        model = models.AssetsInfo
        fields = "__all__"
        exclude = ['now_type','confirmed']


def asset_edit(request, nid):
    """编辑资产信息"""
    row_object = models.AssetsInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = AssetEditInfoForm(instance=row_object)
        return render(request, 'asset_edit.html', {'form': form})
    form = AssetEditInfoForm(instance=row_object, data=request.POST)
    form.save()
    return redirect('/asset/')


def asset_del(request, nid):
    """删除"""
    models.AssetsInfo.objects.filter(id=nid).delete()
    return redirect('/asset/')


def asset_maintain(request, nid):
    """维修登记按钮"""
    row_object = models.AssetsInfo.objects.filter(id=nid).first()
    if not row_object:
        return HttpResponse('Asset not found', status=404)
    if request.method == 'GET':
        # 创建初始化表单的数据
        initial_data = {
            'Reg_number': row_object.Registration_number,
            'Model': row_object.Model,
            'Name': row_object.Name,
            'BelongTo': row_object.BelongTo.id,
            'Applicant': row_object.Applicant,
            # 其他需要预填充的字段
        }
        form = AssetMaintainInfo(initial=initial_data)
        context = {'form': form}
        template_name = 'asset_maintain_add.html' if request.session['info']['type'] == 1 else 'u_asset_maintain_add.html'
        return render(request, template_name, context)

    # POST 请求处理
    form = AssetMaintainInfo(data=request.POST)
    if form.is_valid():
        form.save()
        redirect_url = '/asset/maintain/' if request.session['info']['type'] == 1 else '/user/'
        return redirect(redirect_url)
    else:
        print(form.errors)  # 打印表单错误
        # 重新渲染表单页面，并显示错误信息
        context = {
            'form': form,
            'error_message': '表单数据有误，请检查后重新提交。'
        }
        template_name = 'asset_maintain_add.html' if request.session['info']['type'] == 1 else 'u_asset_maintain_add.html'
        return render(request, template_name, context)


def asset_damage(request, nid):
    """报废登记按钮"""
    row_object = get_object_or_404(models.AssetsInfo, pk=nid)
    if not row_object:
        return HttpResponse('Asset not found', status=404)
    registration_date_str = row_object.Registration_number[:8]  # 登记编号前8位是日期
    # 计算使用年限
    registration_date = datetime.strptime(registration_date_str, '%Y%m%d').date()
    years_used = (now().date() - registration_date).days / 365.25  # 365.25为了消除这几年当中存在闰年的影响
    # 将years_used转换为Decimal并保留三位小数
    years_used = Decimal(years_used).quantize(Decimal('0.000'), rounding=ROUND_HALF_UP)  # 365.25为了消除这几年当中存在闰年的影响

    # 获取 RatioInfo 对象
    ratio_info = row_object.asset_type

    # 计算折旧价格
    depreciation_price = row_object.Unit_price * (1 - Decimal(ratio_info.Ratio) * Decimal(years_used))
    # 保留三位小数
    depreciation_price = depreciation_price.quantize(Decimal('0.000'), rounding=ROUND_HALF_UP)

    if request.method == 'GET':
        initial_data = {
            'Time': now(),
            'Reg_number': row_object,
            'Model': row_object.Model,
            'Name': row_object.Name,
            'Price': row_object.Unit_price,
            'LiftYears': years_used,
            'Type': ratio_info,
            'Applicant': row_object.Applicant,
            'Depreciation_price': depreciation_price,  # 自动填充折旧价格
        }
        form = AssetDamageInfo(initial=initial_data)
        context = {'form': form}
        template_name = 'asset_damage_add.html' if request.session['info']['type'] == 1 else 'u_asset_damage_add.html'
        return render(request, template_name, context)

    # POST 请求处理
    form = AssetDamageInfo(data=request.POST)
    if form.is_valid():
        form.save()
        redirect_url = '/asset/damage/' if request.session['info']['type'] == 1 else '/user/'
        return redirect(redirect_url)
    else:
        print(form.errors)  # 打印表单错误
        # 重新渲染表单页面，并显示错误信息
        context = {
            'form': form,
            'error_message': '表单数据有误，请检查后重新提交。'
        }
        template_name = 'asset_damage_add.html' if request.session['info']['type'] == 1 else 'u_asset_damage_add.html'
        return render(request, template_name, context)


def asset_change(request, nid):
    """转让登记按钮"""
    row_object = models.AssetsInfo.objects.filter(id=nid).first()
    if not row_object:
        return HttpResponse('Asset not found', status=404)

    if request.method == 'GET':
        initial_data = {
            'Reg_number': row_object.Registration_number,
            'Model': row_object.Model,
            'Name': row_object.Name,
            'Applicant': row_object.Applicant,
            'OriginalUnit': row_object.BelongTo,  # 直接传递 Department 实例
        }
        form = AssetChangeInfo(initial=initial_data)
        context = {'form': form}
        template_name = 'asset_change_add.html' if request.session['info']['type'] == 1 else 'u_asset_change_add.html'
        return render(request, template_name, context)

    # POST 请求处理
    form = AssetChangeInfo(data=request.POST)
    if form.is_valid():
        form.save()
        redirect_url = '/asset/change/' if request.session['info']['type'] == 1 else '/user/'
        return redirect(redirect_url)
    else:
        print(form.errors)  # 打印表单错误
        # 重新渲染表单页面，并显示错误信息
        context = {
            'form': form,
            'error_message': '表单数据有误，请检查后重新提交。'
        }
        template_name = 'asset_change_add.html' if request.session['info']['type'] == 1 else 'u_asset_change_add.html'
        return render(request, template_name, context)


@csrf_exempt
def info_verify(request, Registration_number):
    if request.session.get('info', {}).get('type') == 1:
        asset = models.AssetsInfo.objects.filter(Registration_number=Registration_number).first()
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
            li = models.AssetsInfo.objects.filter(now_type=0)
            for i in li:
                # 如果创建时间小于 ti 删除
                if i.create_time < timezone.make_aware(ti, pytz.UTC):
                    i.delete()
            time.sleep(60)
        except Exception as e:
            time.sleep(1)


threading.Thread(target=check_model).start()
