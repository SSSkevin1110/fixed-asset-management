from django.core.exceptions import ValidationError
from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination


class AdminInfo(BootStrapModelForm):
    """管理员信息"""
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.AdminInfo
        fields = ['Username', 'Password', 'confirm_password', 'BelongTo', 'user_type']
        widgets = {
            "Password": forms.PasswordInput(attrs={"type": "password"}),
        }

    def clean_Password(self):
        pwd = self.cleaned_data.get("Password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("Password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            return HttpResponse("密码不一致")
        return confirm


def admin_info(request):
    """用户信息"""

    info_dict = request.session["info"]
    print(info_dict["id"])
    print(info_dict['name'])


    form = AdminInfo()
    data_list = models.AdminInfo.objects.all()
    page_object = Pagination(request, data_list, page_size=2)
    concent = {
        "form": form,
        "data_list": data_list,
        "page_string": page_object.html(),
    }
    return render(request, 'admin.html', concent)


def admin_add(request):
    """添加用户信息"""
    form = AdminInfo()
    if request.method == 'GET':
        return render(request, 'admin_add.html', {'form': form})
    elif request.method == 'POST':
        form = AdminInfo(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/')
        else:
            return HttpResponseBadRequest("表单数据无效")

def admin_edit(request, nid):
    if request.method == "GET":
        row_obj = models.AdminInfo.objects.filter(id=nid).first()
        return render(request, 'admin_edit.html', {'row_obj': row_obj})
    name = md5(request.POST.get("Password"))
    models.AdminInfo.objects.filter(id=nid).update(Password=name)
    return redirect("/admin/")


def admin_del(request, nid):
    models.AdminInfo.objects.filter(id=nid).delete()
    return redirect('/admin/')


def admin_reset(request, nid):
    row_object = models.AdminInfo.objects.filter(id=nid).update(Password='123456')
    return HttpResponse('重置成功')
