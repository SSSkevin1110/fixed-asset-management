from django.shortcuts import render, redirect,HttpResponse
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


class RatioInfoForm(BootStrapModelForm):
    class Meta:
        model = models.RatioInfo
        fields = "__all__"


def ratio(request):
    """预计净残值率展示"""
    ratio_list = models.RatioInfo.objects.all()
    return render(request, 'ratio_list.html', {'ratio_list': ratio_list})

def ratio_add(request):
    if request.method == 'GET':
        form = RatioInfoForm()
        return render(request, "ratio_add.html", {"form": form})
    form = RatioInfoForm(data=request.POST)
    if form.is_valid():
        form.save()
    return redirect('/ratio/')


def ratio_edit(request, nid):
    """编辑"""
    row_object = models.RatioInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = RatioInfoForm(instance=row_object)
        return render(request, 'ratio_edit.html', {'form': form})
    form = RatioInfoForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
    return redirect('/ratio/')


def ratio_del(request, nid):
    """删除"""
    models.RatioInfo.objects.filter(id=nid).delete()
    return redirect('/ratio/')
