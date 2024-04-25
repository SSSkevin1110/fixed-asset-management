from django.shortcuts import render, redirect
from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.pagination import Pagination


class SupplierForm(BootStrapModelForm):
    class Meta:
        model = models.Supplier
        fields = '__all__'


def supplier(request):
    form = SupplierForm()
    data_list = models.Supplier.objects.all()
    page_object = Pagination(request, data_list, page_size=2)
    return render(request, 'supplier.html', {'form': form, 'data_list': data_list, "page_string": page_object.html()})


def supplier_add(request):
    """添加"""
    if request.method == 'GET':
        form = SupplierForm()
        return render(request, 'supplier_add.html', {'form': form})
    form = SupplierForm(data=request.POST)
    if form.is_valid():
        form.save()
    return redirect('/supplier/')


def supplier_edit(request, nid):
    """编辑"""
    row_object = models.Supplier.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = SupplierForm(instance=row_object)
        return render(request, 'supplier_edit.html', {'form': form})
    form = SupplierForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
    return redirect('/supplier/')


def supplier_del(request, nid):
    """删除"""
    models.Supplier.objects.filter(id=nid).delete()
    return redirect('/supplier/')
